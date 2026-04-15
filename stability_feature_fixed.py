"""
Stability Analysis Feature
=========================

Standalone Streamlit feature to analyse photovoltaic stability measurements.

It scans the directory where the script is located for files following:
    <prefix>_Stability (JV)_Stability-D<day>-<device>-<pixel>.txt

It extracts Voc, Jsc, FF and PCE from the summary section, computes the
maximum PCE for each device on each day, and plots Max PCE vs time.

If no matching files are found in the current directory, the user can
enter another folder path or upload .txt files / a .zip archive.
"""

from __future__ import annotations

import os
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
import plotly.express as px
import streamlit as st


@dataclass
class StabilityFileInfo:
    path: Path
    day: int
    device: str
    pixel: str

    @property
    def label(self) -> str:
        return f"Device {self.device} - Pixel {self.pixel}"


STABILITY_PATTERN = re.compile(
    r"^(.*?)_Stability\s*\(JV\)_Stability-D(?P<day>\d+)-(?P<device>[\w\d]+)-(?P<pixel>[\w\d]+)\.txt$",
    re.IGNORECASE,
)


def parse_stability_filename(path: Path) -> StabilityFileInfo | None:
    m = STABILITY_PATTERN.match(path.name)
    if not m:
        return None
    day_str = m.group("day")
    day = int(day_str.lstrip("0")) if day_str else 0
    return StabilityFileInfo(
        path=path,
        day=day,
        device=m.group("device"),
        pixel=m.group("pixel"),
    )


def discover_stability_files(base_dir: Path) -> List[StabilityFileInfo]:
    infos: List[StabilityFileInfo] = []
    for root, _, files in os.walk(base_dir):
        for fname in files:
            if not fname.lower().endswith(".txt"):
                continue
            full_path = Path(root) / fname
            info = parse_stability_filename(full_path)
            if info:
                infos.append(info)
    return infos


def parse_stability_file(path: Path) -> pd.DataFrame:
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return pd.DataFrame(columns=["pce"])

    header_idx = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.lower().startswith("scan") and "jsc" in s.lower():
            header_idx = i
            break

    if header_idx is not None and header_idx + 2 < len(lines):
        header_tokens = re.split(r"\t+", lines[header_idx].strip())
        data_start = header_idx + 2
        records = []
        for row in lines[data_start:]:
            r = row.strip()
            if not r or re.match(r"^[A-Za-z]_", r):
                break
            tokens = re.split(r"\t+", r)
            rec: Dict[str, float] = {}
            for h, t in zip(header_tokens, tokens):
                h_low = h.strip().lower()
                try:
                    val = float(t) if t else None
                except Exception:
                    val = None
                if h_low.startswith("voc"):
                    rec["voc"] = val
                elif h_low.startswith("jsc"):
                    rec["jsc"] = val
                elif h_low.startswith("ff"):
                    rec["ff"] = val
                elif h_low.startswith("eff") or h_low.startswith("pce"):
                    rec["pce"] = val
            if rec.get("pce") is not None:
                records.append(rec)
        if records:
            return pd.DataFrame(records)

    pces: List[float] = []
    for ln in lines:
        m = re.search(r"(pce|efficiency)[^\d]*([\d\.]+)", ln, re.IGNORECASE)
        if m:
            try:
                pces.append(float(m.group(2)))
            except Exception:
                continue
    if pces:
        return pd.DataFrame({"pce": pces})
    return pd.DataFrame(columns=["pce"])


def build_summary_table(infos: List[StabilityFileInfo]) -> pd.DataFrame:
    rows = []
    for info in infos:
        df = parse_stability_file(info.path)
        if df.empty or "pce" not in df.columns:
            continue
        idx = df["pce"].astype(float).idxmax()
        row = {
            "device": info.device,
            "pixel": info.pixel,
            "day": info.day,
            "max_pce": float(df.loc[idx, "pce"]),
        }
        for out_col, src_col in [("max_jsc", "jsc"), ("max_voc", "voc"), ("max_ff", "ff")]:
            if src_col in df.columns:
                try:
                    row[out_col] = float(df.loc[idx, src_col])
                except Exception:
                    row[out_col] = None
        rows.append(row)
    return pd.DataFrame(rows)


def aggregate_by_device_day(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return summary.copy()
    agg_dict = {"max_pce": "max"}
    for col in ["max_jsc", "max_voc", "max_ff"]:
        if col in summary.columns:
            agg_dict[col] = "max"
    return (
        summary.groupby(["device", "day"], as_index=False)
        .agg(agg_dict)
        .sort_values(["device", "day"])
        .reset_index(drop=True)
    )


def main() -> None:
    st.set_page_config(page_title="Stability Analysis", layout="wide")
    st.title("Stability Analysis: Max PCE vs Time")
    st.markdown(
        """
        This tool automatically scans the folder where the script is placed for
        files named like:

        `0001_2026-03-28_13.59.47_Stability (JV)_Stability-D14-40-1A.txt`

        If no matching files are found, you can enter another folder path or
        upload `.txt` files or a `.zip` archive from the sidebar.
        """
    )

    if "stability_infos" not in st.session_state:
        try:
            base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            st.session_state["stability_infos"] = discover_stability_files(base_dir)
        except Exception:
            st.session_state["stability_infos"] = []

    infos: List[StabilityFileInfo] = st.session_state["stability_infos"]

    st.sidebar.header("Data Source")
    st.sidebar.markdown(f"**Found {len(infos)} stability files** in the script folder")

    data_dir = st.sidebar.text_input(
        "Path to data folder (optional)",
        value="",
        help="Enter another folder path only if the script folder does not contain your data.",
    )
    if data_dir:
        base = Path(data_dir).expanduser()
        if base.exists():
            infos = discover_stability_files(base)
        else:
            st.sidebar.error(f"Directory '{data_dir}' does not exist.")
            infos = []

    if not infos:
        st.sidebar.warning(
            "No stability files found. Upload .txt files or a .zip archive below."
        )
        uploaded_files = st.sidebar.file_uploader(
            "Upload stability files",
            type=["txt", "zip"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            tmp_dir = tempfile.mkdtemp()
            uploaded_infos: List[StabilityFileInfo] = []
            for uf in uploaded_files:
                name = uf.name
                if name.lower().endswith(".zip"):
                    try:
                        uf.seek(0)
                        with zipfile.ZipFile(uf) as zf:
                            for nm in zf.namelist():
                                if nm.lower().endswith(".txt"):
                                    file_path = Path(tmp_dir) / Path(nm).name
                                    file_path.parent.mkdir(parents=True, exist_ok=True)
                                    with open(file_path, "wb") as f:
                                        f.write(zf.read(nm))
                                    info = parse_stability_filename(file_path)
                                    if info:
                                        uploaded_infos.append(info)
                    except Exception as e:
                        st.sidebar.error(f"Could not process zip file: {e}")
                elif name.lower().endswith(".txt"):
                    file_path = Path(tmp_dir) / name
                    with open(file_path, "wb") as f:
                        f.write(uf.getvalue())
                    info = parse_stability_filename(file_path)
                    if info:
                        uploaded_infos.append(info)
            infos = uploaded_infos

    if not infos:
        st.info("No valid stability data provided.")
        return

    summary = build_summary_table(infos)
    if summary.empty:
        st.info("No valid PCE values could be extracted from the files.")
        return

    devices = sorted(summary["device"].unique())
    selected_devices = st.sidebar.multiselect(
        "Select devices to display",
        options=devices,
        default=devices,
    )
    summary = summary[summary["device"].isin(selected_devices)]

    agg = aggregate_by_device_day(summary)

    st.header("Maximum PCE vs Day")
    fig = px.line(
        agg,
        x="day",
        y="max_pce",
        color="device",
        markers=True,
        labels={"day": "Day", "max_pce": "Max PCE (%)", "device": "Device"},
        title="Maximum PCE by Device over Time",
    )
    fig.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Show data table"):
        st.dataframe(agg)
        csv_data = agg.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv_data,
            file_name="stability_summary.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    # Use the same auto-launch pattern as your previously working Streamlit file.
    import sys
    import subprocess

    is_streamlit = hasattr(st, "_is_running_with_streamlit") and st._is_running_with_streamlit
    if is_streamlit or os.environ.get("STREAMLIT_AUTORUN") == "1":
        main()
    else:
        os.environ["STREAMLIT_AUTORUN"] = "1"
        subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", os.path.abspath(__file__)],
            env=os.environ.copy(),
        )
        sys.exit()
