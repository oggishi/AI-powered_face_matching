
# Visualization code for thesis graphs
import matplotlib.pyplot as plt
import numpy as np

# Model comparison chart
def plot_model_comparison():
    models = ['ArcFace\n(Ours)', 'FaceNet', 'VGG-Face', 'MediaPipe']
    accuracy = [99.82, 99.20, 98.78, 75.00]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(models, accuracy, color=['#2ecc71', '#3498db', '#9b59b6', '#e74c3c'])
    plt.ylabel('Độ chính xác (%)', fontsize=12)
    plt.title('So sánh độ chính xác các mô hình', fontsize=14, fontweight='bold')
    plt.ylim([70, 100])
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{accuracy[i]:.2f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved model_comparison.png")

# Response time breakdown
def plot_response_time():
    stages = ['Detection', 'Encoding', 'DB Query', 'Other']
    times = [180, 320, 50, 0]  # milliseconds
    colors = ['#3498db', '#2ecc71', '#f39c12', '#95a5a6']
    
    plt.figure(figsize=(8, 8))
    plt.pie(times, labels=stages, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Phân tích thời gian xử lý', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('response_time_breakdown.png', dpi=300, bbox_inches='tight')
    print("✓ Saved response_time_breakdown.png")

# Scalability chart
def plot_scalability():
    num_faces = [10, 50, 100, 500, 1000, 5000, 10000]
    query_time = [5, 12, 25, 85, 165, 420, 850]
    
    plt.figure(figsize=(10, 6))
    plt.plot(num_faces, query_time, marker='o', linewidth=2, markersize=8, color='#2ecc71')
    plt.xlabel('Số lượng khuôn mặt trong CSDL', fontsize=12)
    plt.ylabel('Thời gian truy vấn (ms)', fontsize=12)
    plt.title('Khả năng mở rộng của hệ thống', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.tight_layout()
    plt.savefig('scalability.png', dpi=300, bbox_inches='tight')
    print("✓ Saved scalability.png")

if __name__ == "__main__":
    plot_model_comparison()
    plot_response_time()
    plot_scalability()
    print("\n✓ All visualizations generated")
