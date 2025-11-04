import pandas as pd
import json
import urllib.parse
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

os.makedirs("output_json", exist_ok=True)

def load_sheet(sheet_id, sheet_name):
    """Ambil data dari Google Sheets dan ubah NaN jadi string kosong"""
    sheet_encoded = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_encoded}"
    df = pd.read_csv(url)
    return df.fillna("")

def save_as_json(df, sheet_name):
    """Simpan DataFrame jadi file JSON"""
    data_json = [
        {
            "id": f"dokumen_{i+1}",
            "kelompok_masalah": row.get("Kelompok Masalah", ""),
            "tipe_dokumen": row.get("Tipe Dokumen", ""),
            "hierarki_regulasi": row.get("Hierarki Regulasi", ""),
            "judul": row.get("Judul", ""),
            "bunyi_regulasi": row.get("Bunyi Regulasi", ""),
            "bab": row.get("BAB", ""),
            "nomor": row.get("Nomor", ""),
            "pasal": row.get("Pasal", ""),
            "ayat": row.get("Ayat", ""),
            "tahun_terbit": row.get("Tahun Terbit", ""),
            "jabatan": row.get("Jabatan", "")
        }
        for i, row in df.iterrows()
    ]

    filename = f"output_json/{sheet_name.replace(' ', '_').lower()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_json, f, indent=4, ensure_ascii=False)
    logging.info(f"Disimpan: {filename}")

def main():
    sheet_id = "1T4CQGkjEF9D75SsWgKUDLVqtP9iTaWRU72AguJ7VJe8"
    sheet_names = [
        "JSON STRUCTURE",
        "dataset WI",
        "dataset Analis SDMA",
        "Dataset Penelaah Teknis Kebijakan",
        "Dataset Analis Kebijakan"
    ]

    summary = {"total_sheets": len(sheet_names), "processed": [], "failed": []}

    for name in sheet_names:
        logging.info(f"📄 Memproses sheet: {name}")
        try:
            df = load_sheet(sheet_id, name)
            save_as_json(df, name)
            summary["processed"].append(name)
        except Exception as e:
            logging.error(f"Gagal memproses {name}: {e}")
            summary["failed"].append(name)

    with open("output_json/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    logging.info("Summary disimpan di output_json/summary.json")

if __name__ == "__main__":
    main()
