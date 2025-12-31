import os
import re
import sys

def strip_butterknife_annotations(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except:
        return

    if "@BindView" not in content and "@OnClick" not in content and "ButterKnife" not in content:
        return

    print(f"Stripping ButterKnife from {filepath}...")

    lines = content.split('\n')
    new_lines = []

    for line in lines:
        if line.strip().startswith("import butterknife."):
            continue
        if line.strip().startswith("import com.jakewharton.butterknife."):
            continue

        # Remove @BindView(...) part but keep the rest of the line if it has the field
        # @BindView(R.id.foo) TextView foo; -> TextView foo;
        if "@BindView" in line:
            # Regex to strip annotation
            line = re.sub(r'@BindView\(.*?\)\s*', '', line)

        # Remove @OnClick. Method usually follows.
        # @OnClick(R.id.foo)
        # public void foo()
        if "@OnClick" in line:
             new_lines.append(f"    // TODO: Restore OnClick {line.strip()}")
             continue

        if "ButterKnife.bind" in line:
             new_lines.append(f"        // TODO: Remove ButterKnife.bind")
             continue

        if "Unbinder" in line:
             # remove unbinder fields
             if "unbinder;" in line:
                 continue

        if "unbinder.unbind()" in line:
             continue

        new_lines.append(line)

    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))

def process_directory(root_dir, mode):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(".java"):
                continue

            filepath = os.path.join(root, file)
            # Batching based on first letter of filename
            first_char = file[0].lower()
            if mode == 'batch1':
                if first_char < 'm':
                    strip_butterknife_annotations(filepath)
            elif mode == 'batch2':
                if first_char >= 'm':
                    strip_butterknife_annotations(filepath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 strip_butterknife.py [batch1|batch2]")
        sys.exit(1)

    process_directory("app/src/main/java", sys.argv[1])
