import matplotlib.pyplot as plt
import matplotlib.patches as patches

def add_stick_figure(ax, x, y, label):
    head = patches.Circle((x, y+0.8), 0.3, edgecolor='#3b82f6', facecolor='none', lw=2)
    ax.add_patch(head)
    ax.plot([x, x], [y+0.5, y-0.4], color='#3b82f6', lw=2)
    ax.plot([x-0.4, x+0.4], [y+0.3, y+0.3], color='#3b82f6', lw=2)
    ax.plot([x, x-0.3], [y-0.4, y-1.0], color='#3b82f6', lw=2)
    ax.plot([x, x+0.3], [y-0.4, y-1.0], color='#3b82f6', lw=2)
    ax.text(x, y-1.4, label, color='white', ha='center', fontsize=12, fontweight='bold')

def add_usecase(ax, x, y, w, h, text):
    ellipse = patches.Ellipse((x, y), w, h, edgecolor='#38bdf8', facecolor='#1e293b', lw=2)
    ax.add_patch(ellipse)
    ax.text(x, y, text, color='white', ha='center', va='center', fontsize=11, fontweight='bold', wrap=True)

def generate_use_case():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)

    rect = patches.Rectangle((4, 1), 8, 10, fill=False, edgecolor='#9ca3af', linestyle='--', lw=2)
    ax.add_patch(rect)
    ax.text(8, 10.5, "Cyber Sentry System", color='white', ha='center', fontsize=14, fontweight='bold')

    add_stick_figure(ax, 2, 6, "Security\nAdmin")
    add_stick_figure(ax, 14, 6, "Background\nGuard Service")

    y_pos = [8.5, 6.8, 5.1, 3.4, 1.7]
    use_cases = [
        "Scan Threat Target\n(URL/Domain/IPv6)",
        "Audit Local PC\nProcesses",
        "View System\nDiagnostics",
        "Monitor DNS\nSinkhole Logs",
        "Manage Blacklist\n& Whitelist"
    ]

    for y, text in zip(y_pos, use_cases):
        add_usecase(ax, 8, y, 6, 1.2, text)
        ax.plot([2.5, 5], [6, y], color='#4b5563', lw=1.5, zorder=0)

    ax.plot([13.5, 11], [6, 3.4], color='#4b5563', lw=1.5, zorder=0) 
    ax.plot([13.5, 11], [6, 6.8], color='#4b5563', lw=1.5, zorder=0) 

    plt.savefig('use_case_diagram.png', facecolor='#0f172a', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated: use_case_diagram.png")

def generate_sequence():
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)

    lifelines = [("User", 2), ("GUI Dashboard", 6), ("Threat Scanner (ML)", 10), ("Network & OS", 14)]

    for name, x in lifelines:
        rect = patches.Rectangle((x-1.5, 10.5), 3, 1, fill=True, color='#1e293b', ec='#3b82f6', lw=2)
        ax.add_patch(rect)
        ax.text(x, 11, name, color='white', ha='center', va='center', fontweight='bold', fontsize=11)
        ax.plot([x, x], [0.5, 10.5], color='#6b7280', linestyle='--', lw=1.5)

    def add_msg(y, x1, x2, text, reverse=False, self_call=False):
        if self_call:
            ax.plot([x1, x1+0.8, x1+0.8, x1], [y, y, y-0.6, y-0.6], color='#38bdf8', lw=2)
            ax.plot(x1, y-0.6, marker='<', color='#38bdf8', markersize=8)
            ax.text(x1+1.0, y-0.3, text, color='white', va='center', fontsize=10)
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color='#38bdf8', lw=2))
            ax.text((x1+x2)/2, y+0.2, text, color='white', ha='center', fontsize=10)

    add_msg(9.5, 2, 6, "1. Submit Target Domain")
    add_msg(8.5, 6, 10, "2. Request Threat Analysis")
    add_msg(7.5, 10, 14, "3. Resolve IPv4/IPv6")
    add_msg(6.5, 14, 10, "4. Return Structural IPs", reverse=True)
    add_msg(5.5, 10, 10, "5. Extract 30 Dataset Features", self_call=True)
    add_msg(4.0, 10, 10, "6. Execute 7-Model Predictors", self_call=True)
    add_msg(2.5, 10, 6, "7. Return Consensus Verdict", reverse=True)
    add_msg(1.5, 6, 2, "8. Display Threat Report", reverse=True)

    ax.add_patch(patches.Rectangle((5.9, 1.3), 0.2, 8.4, fill=True, color='#475569'))
    ax.add_patch(patches.Rectangle((9.9, 2.3), 0.2, 6.4, fill=True, color='#475569'))
    ax.add_patch(patches.Rectangle((13.9, 6.3), 0.2, 1.4, fill=True, color='#475569'))

    plt.savefig('sequence_diagram.png', facecolor='#0f172a', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated: sequence_diagram.png")

def generate_architecture():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)

    def draw_block(x, y, w, h, title, text="", color='#1e293b', ec='#3b82f6'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", edgecolor=ec, facecolor=color, lw=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.4, title, ha='center', va='top', color='white', fontsize=12, fontweight='bold')
        if text:
            ax.text(x + w/2, y + h/2 - 0.2, text, ha='center', va='center', color='#cbd5e1', fontsize=10, wrap=True)

    draw_block(5, 9.5, 6, 1.5, "Presentation Layer", "CustomTkinter GUI Dashboard\n(App Views & Controls)")

    draw_block(1, 6, 14, 2.5, "Business Logic Core (Controllers)", ec='#8b5cf6', color='#2e1065')
    draw_block(1.5, 6.2, 3, 1.2, "Threat Scanner")
    draw_block(5, 6.2, 3, 1.2, "Background Guard")
    draw_block(8.5, 6.2, 3, 1.2, "Network Log Engine")
    draw_block(12, 6.2, 2.5, 1.2, "System Diags")

    draw_block(2, 2, 7, 2.5, "Machine Learning Engine", "LR, DT, RF, SVM, KNN, GB, MLP\n(Sklearn Pipeline)", color='#064e3b', ec='#10b981')
    draw_block(10, 2, 4, 2.5, "Data Store & Policies", "phishing_features.csv\nBlacklist / Whitelist", color='#7f1d1d', ec='#ef4444')

    ax.annotate('', xy=(8, 8.5), xytext=(8, 9.5), arrowprops=dict(arrowstyle="<->", color='#9ca3af', lw=2))
    ax.annotate('', xy=(5.5, 4.5), xytext=(4, 6), arrowprops=dict(arrowstyle="<->", color='#9ca3af', lw=2))
    ax.annotate('', xy=(12, 4.5), xytext=(12, 6), arrowprops=dict(arrowstyle="<->", color='#9ca3af', lw=2))

    plt.savefig('architecture_diagram.png', facecolor='#0f172a', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated: architecture_diagram.png")

def generate_flowchart():
    fig, ax = plt.subplots(figsize=(14, 12))
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)

    def draw_flow_node(x, y, w, h, text, shape="rect", color='#1e293b'):
        if shape == "rect":
            p = patches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.1", ec='#3b82f6', fc=color, lw=2)
        elif shape == "oval":
            p = patches.Ellipse((x, y), w, h, ec='#10b981', fc=color, lw=2)
        elif shape == "diamond":
            p = patches.Polygon([[x, y+h/2], [x+w/2, y], [x, y-h/2], [x-w/2, y]], ec='#f59e0b', fc=color, lw=2)
        ax.add_patch(p)
        ax.text(x, y, text, ha='center', va='center', color='white', fontsize=10, fontweight='bold', wrap=True)

    def flow_arrow(x1, y1, x2, y2, text=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color='#9ca3af', lw=2))
        if text:
            ax.text((x1+x2)/2 + 0.2, (y1+y2)/2, text, color='#38bdf8', fontsize=10, fontweight='bold')

    draw_flow_node(8, 15, 3, 1, "Start Cyber Sentry", "oval")
    flow_arrow(8, 14.5, 8, 13.5)
    draw_flow_node(8, 13, 4, 1, "Load Configuration,\nBlacklist & Whitelist")
    flow_arrow(8, 12.5, 8, 11.5)
    draw_flow_node(8, 11, 4, 1, "Train 7 ML Models\n(phishing_features.csv)")
    flow_arrow(8, 10.5, 8, 9.5)
    draw_flow_node(8, 9, 4, 1.5, "Wait for User Event\n(GUI Event Loop)", "diamond")

    flow_arrow(6, 9, 4, 9, "Background Guard")
    draw_flow_node(2.5, 9, 3, 1.5, "Intercept Local\nSocket", "diamond")
    flow_arrow(2.5, 8.25, 2.5, 6.5, "In Blacklist?")
    draw_flow_node(2.5, 6, 3, 1, "Sinkhole Connection")
    flow_arrow(2.5, 5.5, 2.5, 4.5)
    draw_flow_node(2.5, 4, 3, 1, "Log to Interface")
    ax.plot([1, 1], [4, 9], color='#9ca3af', lw=2)
    ax.plot([1, 2.5], [9, 9], color='#9ca3af', lw=2)
    ax.annotate('', xy=(1, 9), xytext=(1, 4), arrowprops=dict(arrowstyle="-", color='#9ca3af', lw=2))

    flow_arrow(8, 8.25, 8, 7, "User Input Target")
    draw_flow_node(8, 6.5, 3, 1, "Extract URL Features")
    flow_arrow(8, 6, 8, 5)
    draw_flow_node(8, 4.5, 3, 1, "ML Ensemble Predict")
    flow_arrow(8, 4, 8, 3)
    draw_flow_node(8, 2.5, 3, 1, "Show Verdict")
    ax.plot([8, 8], [2, 1], color='#9ca3af', lw=2)
    ax.plot([8, 15], [1, 1], color='#9ca3af', lw=2)
    ax.plot([15, 15], [1, 9], color='#9ca3af', lw=2)
    ax.annotate('', xy=(10, 9), xytext=(15, 9), arrowprops=dict(arrowstyle="->", color='#9ca3af', lw=2))

    ax.annotate('', xy=(12.5, 10.5), xytext=(10, 9), arrowprops=dict(arrowstyle="->", color='#9ca3af', lw=2, connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(11, 10, "Diagnostics Tab", color='#38bdf8', fontsize=10, fontweight='bold')
    draw_flow_node(13.5, 10.5, 3, 1, "Fetch OS CPU/RAM")
    flow_arrow(13.5, 10, 13.5, 8.5)
    draw_flow_node(13.5, 8, 3, 1, "Update Progress Bars")
    ax.plot([13.5, 13.5], [7.5, 1], color='#9ca3af', lw=2)

    plt.title('System Flowchart', fontsize=22, fontweight='bold', color='white')
    plt.savefig('system_flowchart.png', facecolor='#0f172a', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated: system_flowchart.png")

def generate_activity():
    fig, ax = plt.subplots(figsize=(10, 14))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)

    ax.add_patch(patches.Circle((5, 15.5), 0.3, color='black'))
    ax.add_patch(patches.Circle((5, 0.5), 0.3, color='black'))
    ax.add_patch(patches.Circle((5, 0.5), 0.4, fill=False, edgecolor='black', lw=2))

    def act_node(y, text):
        p = patches.FancyBboxPatch((3, y-0.4), 4, 0.8, boxstyle="round,pad=0.1", ec='black', fc='#e2e8f0', lw=2)
        ax.add_patch(p)
        ax.text(5, y, text, ha='center', va='center', color='black', fontsize=10, fontweight='bold', wrap=True)

    def act_arrow(y1, y2):
        ax.annotate('', xy=(5, y2), xytext=(5, y1), arrowprops=dict(arrowstyle="->", color='black', lw=2))

    act_arrow(15.2, 14.4)
    act_node(14, "Input Target Domain / URL")
    act_arrow(13.6, 12.4)
    act_node(12, "Resolve IPv4 & IPv6 Nodes")
    act_arrow(11.6, 10.4)
    act_node(10, "Synthesize 30-Feature Matrix")
    act_arrow(9.6, 8.5)

    ax.add_patch(patches.Rectangle((1.5, 8.4), 7, 0.2, color='black'))
    ax.add_patch(patches.Rectangle((1.5, 5.4), 7, 0.2, color='black'))

    models = ["LR", "DT", "RF", "SVM", "KNN", "GB", "MLP"]
    for i, m in enumerate(models):
        x_pos = 2 + i * 1.0
        ax.plot([5, x_pos], [8.4, 8.4], color='black', lw=2)
        ax.annotate('', xy=(x_pos, 7.5), xytext=(x_pos, 8.4), arrowprops=dict(arrowstyle="-", color='black', lw=2))
        p = patches.FancyBboxPatch((x_pos-0.4, 6.5), 0.8, 1.0, boxstyle="round,pad=0.05", ec='black', fc='#e2e8f0', lw=1.5)
        ax.add_patch(p)
        ax.text(x_pos, 7, m, ha='center', va='center', color='black', fontsize=9, fontweight='bold')
        ax.annotate('', xy=(x_pos, 5.6), xytext=(x_pos, 6.5), arrowprops=dict(arrowstyle="->", color='black', lw=2))

    act_arrow(5.4, 4.4)
    act_node(4, "Aggregate Predictions\n(Consensus Check >= 4)")
    act_arrow(3.6, 2.4)

    p = patches.Polygon([[5, 2.8], [6, 2.2], [5, 1.6], [4, 2.2]], ec='black', fc='#fcd34d', lw=2)
    ax.add_patch(p)
    ax.text(5, 2.2, "Threat\nLevel?", ha='center', va='center', color='black', fontsize=9, fontweight='bold')

    ax.plot([6, 7.5], [2.2, 2.2], color='black', lw=2)
    ax.text(6.75, 2.4, "[>=4 Flags]", fontsize=8, color='black')
    ax.plot([4, 2.5], [2.2, 2.2], color='black', lw=2)
    ax.text(3.25, 2.4, "[<4 Flags]", fontsize=8, color='black')

    p1 = patches.FancyBboxPatch((6.5, 1.0), 2, 0.6, boxstyle="round,pad=0.1", ec='black', fc='#fca5a5', lw=2)
    ax.add_patch(p1)
    ax.text(7.5, 1.3, "Mark as\nCRITICAL", ha='center', va='center', color='black', fontsize=9, fontweight='bold')

    p2 = patches.FancyBboxPatch((1.5, 1.0), 2, 0.6, boxstyle="round,pad=0.1", ec='black', fc='#bbf7d0', lw=2)
    ax.add_patch(p2)
    ax.text(2.5, 1.3, "Mark as\nSAFE", ha='center', va='center', color='black', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(7.5, 0.5), xytext=(7.5, 1.0), arrowprops=dict(arrowstyle="-", color='black', lw=2))
    ax.annotate('', xy=(2.5, 0.5), xytext=(2.5, 1.0), arrowprops=dict(arrowstyle="-", color='black', lw=2))
    ax.plot([2.5, 7.5], [0.5, 0.5], color='black', lw=2)
    ax.annotate('', xy=(4.6, 0.5), xytext=(5, 0.5), arrowprops=dict(arrowstyle="<-", color='black', lw=2))

    plt.title('Threat Scanning Activity Diagram', fontsize=18, fontweight='bold', color='black', y=1.02)
    fig.patch.set_facecolor('white')
    plt.savefig('activity_diagram.png', facecolor='white', bbox_inches='tight', dpi=300)
    plt.close()
    print("Generated: activity_diagram.png")

if __name__ == "__main__":
    print("Initializing diagram rendering sequence...")
    generate_use_case()
    generate_sequence()
    generate_architecture()
    generate_flowchart()
    generate_activity()
    print("All architecture and logical diagrams successfully rendered.")