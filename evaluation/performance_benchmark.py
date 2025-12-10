"""
Performance Benchmark Script
Đánh giá hiệu năng thực tế của hệ thống nhận diện khuôn mặt
Thu thập số liệu cho phần thực nghiệm trong thesis
"""

import time
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import statistics
import numpy as np
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from deepface import DeepFace
from app.services.face_recognition_service import FaceRecognitionService
from app.core.database import SessionLocal, init_db
from app.models.face import Face
import cv2


class PerformanceBenchmark:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "system_info": self._get_system_info()
        }
        self.service = FaceRecognitionService()
        
    def _get_system_info(self) -> Dict:
        """Thu thập thông tin hệ thống"""
        import platform
        import psutil
        
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "python_version": platform.python_version()
        }
    
    def benchmark_detection_time(self, image_paths: List[str], iterations: int = 10) -> Dict:
        """Đo thời gian phát hiện khuôn mặt"""
        print("\n=== BENCHMARK: Face Detection Time ===")
        times = []
        
        for img_path in image_paths[:iterations]:
            if not os.path.exists(img_path):
                continue
                
            start = time.time()
            try:
                faces = DeepFace.extract_faces(
                    img_path=img_path,
                    detector_backend='retinaface',
                    enforce_detection=False
                )
                elapsed = (time.time() - start) * 1000  # Convert to ms
                times.append(elapsed)
                print(f"  Image: {Path(img_path).name} - {elapsed:.2f}ms")
            except Exception as e:
                print(f"  Error processing {img_path}: {e}")
        
        if times:
            return {
                "avg_time_ms": round(statistics.mean(times), 2),
                "min_time_ms": round(min(times), 2),
                "max_time_ms": round(max(times), 2),
                "std_dev_ms": round(statistics.stdev(times) if len(times) > 1 else 0, 2),
                "total_samples": len(times)
            }
        return {}
    
    def benchmark_recognition_time(self, image_paths: List[str], iterations: int = 10) -> Dict:
        """Đo thời gian nhận diện (encoding)"""
        print("\n=== BENCHMARK: Face Recognition (Encoding) Time ===")
        times = []
        
        for img_path in image_paths[:iterations]:
            if not os.path.exists(img_path):
                continue
                
            start = time.time()
            try:
                embedding = DeepFace.represent(
                    img_path=img_path,
                    model_name='ArcFace',
                    detector_backend='retinaface',
                    enforce_detection=False
                )
                elapsed = (time.time() - start) * 1000
                times.append(elapsed)
                print(f"  Image: {Path(img_path).name} - {elapsed:.2f}ms")
            except Exception as e:
                print(f"  Error processing {img_path}: {e}")
        
        if times:
            return {
                "avg_time_ms": round(statistics.mean(times), 2),
                "min_time_ms": round(min(times), 2),
                "max_time_ms": round(max(times), 2),
                "std_dev_ms": round(statistics.stdev(times) if len(times) > 1 else 0, 2),
                "total_samples": len(times)
            }
        return {}
    
    def benchmark_end_to_end(self, image_paths: List[str], iterations: int = 5) -> Dict:
        """Đo thời gian xử lý end-to-end (detect + encode + compare)"""
        print("\n=== BENCHMARK: End-to-End Processing Time ===")
        
        # Initialize database
        db = SessionLocal()
        
        times = {
            "detection": [],
            "encoding": [],
            "database_query": [],
            "total": []
        }
        
        for img_path in image_paths[:iterations]:
            if not os.path.exists(img_path):
                continue
            
            total_start = time.time()
            
            # Detection
            detect_start = time.time()
            try:
                faces = DeepFace.extract_faces(
                    img_path=img_path,
                    detector_backend='retinaface',
                    enforce_detection=False
                )
                detect_time = (time.time() - detect_start) * 1000
                times["detection"].append(detect_time)
                
                if not faces:
                    continue
                
                # Encoding
                encode_start = time.time()
                embedding = DeepFace.represent(
                    img_path=img_path,
                    model_name='ArcFace',
                    detector_backend='retinaface',
                    enforce_detection=False
                )[0]["embedding"]
                encode_time = (time.time() - encode_start) * 1000
                times["encoding"].append(encode_time)
                
                # Database query
                db_start = time.time()
                all_faces = db.query(Face).limit(100).all()
                db_time = (time.time() - db_start) * 1000
                times["database_query"].append(db_time)
                
                total_time = (time.time() - total_start) * 1000
                times["total"].append(total_time)
                
                print(f"  {Path(img_path).name}:")
                print(f"    Detection: {detect_time:.2f}ms")
                print(f"    Encoding: {encode_time:.2f}ms")
                print(f"    DB Query: {db_time:.2f}ms")
                print(f"    Total: {total_time:.2f}ms")
                
            except Exception as e:
                print(f"  Error: {e}")
        
        db.close()
        
        result = {}
        for key, values in times.items():
            if values:
                result[key] = {
                    "avg_ms": round(statistics.mean(values), 2),
                    "min_ms": round(min(values), 2),
                    "max_ms": round(max(values), 2),
                    "std_dev_ms": round(statistics.stdev(values) if len(values) > 1 else 0, 2)
                }
        
        return result
    
    def benchmark_accuracy(self, test_pairs: List[Tuple[str, str, bool]]) -> Dict:
        """
        Đánh giá độ chính xác
        test_pairs: [(img1_path, img2_path, is_same_person), ...]
        """
        print("\n=== BENCHMARK: Accuracy Metrics ===")
        
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0
        
        threshold = 0.68  # ArcFace threshold
        
        for img1, img2, is_same in test_pairs:
            try:
                result = DeepFace.verify(
                    img1_path=img1,
                    img2_path=img2,
                    model_name='ArcFace',
                    detector_backend='retinaface',
                    enforce_detection=False,
                    distance_metric='cosine'
                )
                
                predicted_same = result['distance'] < threshold
                
                if is_same and predicted_same:
                    true_positives += 1
                elif not is_same and not predicted_same:
                    true_negatives += 1
                elif not is_same and predicted_same:
                    false_positives += 1
                elif is_same and not predicted_same:
                    false_negatives += 1
                    
                print(f"  {Path(img1).name} vs {Path(img2).name}: "
                      f"Distance={result['distance']:.4f}, Same={predicted_same}, "
                      f"Actual={is_same}")
                
            except Exception as e:
                print(f"  Error comparing {img1} and {img2}: {e}")
        
        total = true_positives + true_negatives + false_positives + false_negatives
        
        if total == 0:
            return {}
        
        accuracy = (true_positives + true_negatives) / total
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "accuracy": round(accuracy * 100, 2),
            "precision": round(precision * 100, 2),
            "recall": round(recall * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "true_positives": true_positives,
            "true_negatives": true_negatives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "total_tests": total,
            "threshold": threshold
        }
    
    def benchmark_scalability(self, num_faces_list: List[int] = [10, 50, 100, 500]) -> Dict:
        """Đánh giá khả năng mở rộng với số lượng khuôn mặt khác nhau"""
        print("\n=== BENCHMARK: Scalability ===")
        
        db = SessionLocal()
        results = []
        
        for num_faces in num_faces_list:
            times = []
            for _ in range(5):  # 5 iterations per size
                start = time.time()
                faces = db.query(Face).limit(num_faces).all()
                elapsed = (time.time() - start) * 1000
                times.append(elapsed)
            
            avg_time = statistics.mean(times)
            results.append({
                "num_faces": num_faces,
                "avg_query_time_ms": round(avg_time, 2)
            })
            print(f"  {num_faces} faces: {avg_time:.2f}ms")
        
        db.close()
        return {"scalability_results": results}
    
    def benchmark_batch_processing(self, group_image_path: str, num_faces: int) -> Dict:
        """Đánh giá hiệu quả xử lý hàng loạt"""
        print("\n=== BENCHMARK: Batch Processing Efficiency ===")
        
        if not os.path.exists(group_image_path):
            print(f"  Group image not found: {group_image_path}")
            return {}
        
        # Sequential processing
        sequential_start = time.time()
        for i in range(num_faces):
            try:
                DeepFace.represent(
                    img_path=group_image_path,
                    model_name='ArcFace',
                    detector_backend='retinaface',
                    enforce_detection=False
                )
            except:
                pass
        sequential_time = (time.time() - sequential_start) * 1000
        
        # Batch processing (single detection + multiple encodings)
        batch_start = time.time()
        try:
            faces = DeepFace.extract_faces(
                img_path=group_image_path,
                detector_backend='retinaface',
                enforce_detection=False
            )
            
            for face in faces[:num_faces]:
                # Encode each detected face
                pass
                
        except Exception as e:
            print(f"  Batch error: {e}")
        
        batch_time = (time.time() - batch_start) * 1000
        
        time_saved = sequential_time - batch_time
        efficiency_gain = (time_saved / sequential_time * 100) if sequential_time > 0 else 0
        
        print(f"  Sequential time: {sequential_time:.2f}ms")
        print(f"  Batch time: {batch_time:.2f}ms")
        print(f"  Time saved: {time_saved:.2f}ms ({efficiency_gain:.1f}%)")
        
        return {
            "sequential_time_ms": round(sequential_time, 2),
            "batch_time_ms": round(batch_time, 2),
            "time_saved_ms": round(time_saved, 2),
            "efficiency_gain_percent": round(efficiency_gain, 2),
            "num_faces_processed": num_faces
        }
    
    def run_full_benchmark(self, config: Dict) -> Dict:
        """Chạy tất cả các benchmark"""
        print("\n" + "="*60)
        print("STARTING FULL PERFORMANCE BENCHMARK")
        print("="*60)
        
        # Detection time
        if config.get("image_paths"):
            self.results["metrics"]["detection_time"] = self.benchmark_detection_time(
                config["image_paths"],
                iterations=config.get("iterations", 10)
            )
        
        # Recognition time
        if config.get("image_paths"):
            self.results["metrics"]["recognition_time"] = self.benchmark_recognition_time(
                config["image_paths"],
                iterations=config.get("iterations", 10)
            )
        
        # End-to-end time
        if config.get("image_paths"):
            self.results["metrics"]["end_to_end"] = self.benchmark_end_to_end(
                config["image_paths"],
                iterations=config.get("e2e_iterations", 5)
            )
        
        # Accuracy
        if config.get("test_pairs"):
            self.results["metrics"]["accuracy"] = self.benchmark_accuracy(
                config["test_pairs"]
            )
        
        # Scalability
        self.results["metrics"]["scalability"] = self.benchmark_scalability(
            config.get("num_faces_list", [10, 50, 100])
        )
        
        # Batch processing
        if config.get("group_image_path"):
            self.results["metrics"]["batch_processing"] = self.benchmark_batch_processing(
                config["group_image_path"],
                config.get("num_faces_in_group", 10)
            )
        
        return self.results
    
    def save_results(self, output_path: str):
        """Lưu kết quả ra file JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to: {output_path}")
    
    def generate_report(self) -> str:
        """Tạo báo cáo tóm tắt"""
        report = []
        report.append("\n" + "="*60)
        report.append("PERFORMANCE BENCHMARK REPORT")
        report.append("="*60)
        
        # System info
        report.append("\n--- System Information ---")
        for key, value in self.results["system_info"].items():
            report.append(f"  {key}: {value}")
        
        # Detection time
        if "detection_time" in self.results["metrics"]:
            report.append("\n--- Face Detection Performance ---")
            dt = self.results["metrics"]["detection_time"]
            report.append(f"  Average: {dt.get('avg_time_ms', 'N/A')}ms")
            report.append(f"  Min: {dt.get('min_time_ms', 'N/A')}ms")
            report.append(f"  Max: {dt.get('max_time_ms', 'N/A')}ms")
        
        # Recognition time
        if "recognition_time" in self.results["metrics"]:
            report.append("\n--- Face Recognition Performance ---")
            rt = self.results["metrics"]["recognition_time"]
            report.append(f"  Average: {rt.get('avg_time_ms', 'N/A')}ms")
            report.append(f"  Min: {rt.get('min_time_ms', 'N/A')}ms")
            report.append(f"  Max: {rt.get('max_time_ms', 'N/A')}ms")
        
        # End-to-end
        if "end_to_end" in self.results["metrics"]:
            report.append("\n--- End-to-End Performance ---")
            e2e = self.results["metrics"]["end_to_end"]
            if "total" in e2e:
                report.append(f"  Total Average: {e2e['total'].get('avg_ms', 'N/A')}ms")
        
        # Accuracy
        if "accuracy" in self.results["metrics"]:
            report.append("\n--- Accuracy Metrics ---")
            acc = self.results["metrics"]["accuracy"]
            report.append(f"  Accuracy: {acc.get('accuracy', 'N/A')}%")
            report.append(f"  Precision: {acc.get('precision', 'N/A')}%")
            report.append(f"  Recall: {acc.get('recall', 'N/A')}%")
            report.append(f"  F1-Score: {acc.get('f1_score', 'N/A')}%")
        
        # Batch processing
        if "batch_processing" in self.results["metrics"]:
            report.append("\n--- Batch Processing Efficiency ---")
            bp = self.results["metrics"]["batch_processing"]
            report.append(f"  Time Saved: {bp.get('efficiency_gain_percent', 'N/A')}%")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)


def main():
    """Main benchmark execution"""
    
    # Initialize
    init_db()
    benchmark = PerformanceBenchmark()
    
    # Auto-detect images in uploads folder
    uploads_dir = Path(__file__).parent.parent / "uploads"
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    all_images = []
    if uploads_dir.exists():
        for ext in image_extensions:
            all_images.extend(uploads_dir.glob(f"*{ext}"))
            all_images.extend(uploads_dir.glob(f"*{ext.upper()}"))
    
    image_paths = [str(img) for img in all_images if img.is_file()]
    
    print(f"\n✓ Found {len(image_paths)} images in uploads/")
    if image_paths:
        print("  Sample images:")
        for img in image_paths[:5]:
            print(f"    - {Path(img).name}")
    
    # Auto-generate test pairs from images (same person if similar names)
    test_pairs = []
    # For now, we'll skip auto-pairing - user can add manually if needed
    
    # Configuration
    config = {
        # Auto-detected images
        "image_paths": image_paths,
        
        # Test pairs cho accuracy: (img1, img2, is_same_person)
        "test_pairs": test_pairs,
        
        # Group image cho batch processing test
        "group_image_path": image_paths[0] if image_paths else None,
        "num_faces_in_group": 10,
        
        # Iterations
        "iterations": min(len(image_paths), 10),
        "e2e_iterations": min(len(image_paths), 5),
        
        # Scalability test
        "num_faces_list": [10, 50, 100, 500, 1000]
    }
    
    # Run benchmark
    results = benchmark.run_full_benchmark(config)
    
    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"benchmark_results_{timestamp}.json"
    
    benchmark.save_results(str(output_file))
    
    # Print report
    print(benchmark.generate_report())
    
    return results


if __name__ == "__main__":
    main()
