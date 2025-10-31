import os
import pandas as pd
from utils import getSequence, filter_images_in_bbox, saveImages

# === Define scenes with their sequences, center, and bounding box distance ===
scenes = {
    "spagna_train0": {
        "sequences": ['S0kbYi8VQ_WxGBZSOrY3Wg', 'n4k0JDQfdeItNMf9OOwCUQ'],
        "center": [41.905865911345124, 12.482201692670273],
        "dist": 0.00095
    },
    "campus_train0": {
        "sequences": ['5kb1M1svQmCdlwVYX6iP4Q'],
        "center": [41.90388498, 12.51466155],
        "dist": 0.00195
    },
}

# === Define per-sequence cutoffs (milliseconds since epoch) ===
cutoffs = {
    "gF8nHR2-5AgrrYdJgHGepA": (1518857085215, 1518857097399),
    "5kb1M1svQmCdlwVYX6iP4Q": (1541843523403, 1541843620173),
    "S0kbYi8VQ_WxGBZSOrY3Wg": (1550127484107, 1550127634070),
}


def apply_time_filter(folder, seq_id):
    """Filter metadata.csv and images in a folder by capture time cutoff."""
    if seq_id not in cutoffs:
        return

    min_ms, max_ms = cutoffs[seq_id]
    csv_path = os.path.join(folder, "metadata.csv")

    if not os.path.exists(csv_path):
        print(f"   [WARN] No metadata.csv found in {folder}")
        return

    df = pd.read_csv(csv_path)

    # Keep only rows inside cutoff
    df_filtered = df[(df["captured_at"] >= min_ms) & (df["captured_at"] <= max_ms)]

    # Remove images outside cutoff
    to_remove = set(df["id"]) - set(df_filtered["id"])
    for img_id in to_remove:
        img_path = os.path.join(folder, f"{img_id}.jpg")
        if os.path.exists(img_path):
            os.remove(img_path)

    # Overwrite metadata.csv
    df_filtered.to_csv(csv_path, index=False)
    print(f"   -> Filtered {len(df)} → {len(df_filtered)} images for {seq_id}")


def main():
    for scene_name, scene_info in scenes.items():
        print(f"\n=== Processing {scene_name} ===")
        for seq_id in scene_info["sequences"]:
            print(f"Sequence {seq_id} ...")
            seq_data = getSequence(seq_id)

            # Spatial filter
            filtered = filter_images_in_bbox(
                seq_data, scene_info["center"], scene_info["dist"], scene_info["dist"]
            )

            if not filtered["data"]:
                print(f" -> No images kept inside bbox for {seq_id}")
                continue

            folder = f"vbr_mapillary_overlap/{scene_name}/{seq_id}"
            os.makedirs(folder, exist_ok=True)

            print(f" -> Saving {len(filtered['data'])} images to {folder}")
            saveImages(folder, filtered, downloadImages=True)

            # Apply capture time filter after download
            apply_time_filter(folder, seq_id)


if __name__ == "__main__":
    main()
