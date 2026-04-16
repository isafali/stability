# 🚀 Quick Start Guide - PV Stability Analysis Tool

## ⚡ Get Started in 5 Minutes

### Prerequisites
- Python 3.12+ (already configured)
- Virtual environment with dependencies (already installed)
- Streamlit app running on http://localhost:8501

---

## 🎯 Quick Workflow

### 1️⃣ Launch the App
```bash
cd /workspaces/stability
streamlit run stability_feature_fixed.py
```
✅ Opens on http://localhost:8501

---

### 2️⃣ Load Your Data

**Option A: From Script Folder**
- Sidebar automatically scans for files
- Shows: "✓ Found N files"

**Option B: From Custom Folder**
1. Select "Custom Folder" in sidebar
2. Enter path: `/path/to/your/data`
3. Wait for: "✓ Found N files"

**Option C: Upload Files**
1. Select "Upload Files" in sidebar
2. Drag & drop .txt files or .zip archive
3. Wait for: "✓ Processed N files"

---

### 3️⃣ Explore Raw Data

Go to **Tab 2: 📋 Raw Data**
- See all measurements extracted from your files
- Check data structure: device, pixel, day, scan, jsc, voc, ff, pce
- Filter by device
- Navigate pages

**What to look for:**
- ✓ Correct parameter extraction
- ✓ All 4 values present (Jsc, Voc, FF, PCE)
- ✓ Data range looks reasonable

---

### 4️⃣ View Trends

Go to **Tab 1: 📈 Analysis**
1. Select devices from dropdown
2. Toggle "Show all measurement points" if desired
3. View interactive plots:
   - PCE vs Day
   - Jsc vs Day
   - Voc vs Day
   - Fill Factor vs Day

**Hover over plots** to see exact values

---

### 5️⃣ Apply Filters

Go to **Tab 3: 🔍 Filtering**

**Step 1: Set Filter Ranges**
```
Jsc:  Min [20] Max [50]   ← Adjust these values
Voc:  Min [0.5] Max [1.5]
FF:   Min [50] Max [85]
PCE:  Min [5] Max [30]
```

Recommended ranges are shown below each input

**Step 2: Click "🔄 Apply Filters"**

**Step 3: Check Results**
- View quality metrics
- See how many records removed
- Check removal percentage

---

### 6️⃣ Analyze Statistics

Go to **Tab 4: 📊 Statistics**
- View overall statistics for all parameters
- See statistics by device
- See statistics by day
- Check mean, median, std dev, min, max

---

### 7️⃣ Export Results

Go to **Tab 5: 💾 Export**

**Available Downloads:**
1. Raw Data (CSV) - Original unfiltered data
2. Filtered Data (CSV) - Data after your filters
3. By Device (CSV) - Aggregated by device
4. By Day (CSV) - Aggregated by measurement day

Click button → File downloads automatically

---

## 📊 Typical Use Cases

### Use Case 1: Verify Data Loading
1. Open Tab 2 (Raw Data)
2. Check that all columns present: device, pixel, day, scan, jsc, voc, ff, pce
3. Verify numbers are reasonable
4. If missing data → Check file format

### Use Case 2: Remove Bad Data
1. Open Tab 3 (Filtering)
2. Look at "Recommended" ranges
3. Adjust if needed (e.g., PCE 10-25% instead of 5-30)
4. Click "Apply Filters"
5. Check "Removal %" to verify reasonable amount removed

### Use Case 3: Analyze Stability
1. Open Tab 1 (Analysis)
2. Select interested devices
3. Toggle "Show all measurement points" OFF
4. View trend lines → Identify stable vs degrading devices

### Use Case 4: Export for Further Analysis
1. Apply filters as desired
2. Go to Tab 5 (Export)
3. Download "By Day (CSV)" for time-series analysis
4. Open in Excel/Python for advanced analysis

### Use Case 5: Generate Report
1. Prepare analysis (filters applied, devices selected)
2. Go to Tab 5 (Export)
3. Download all CSV files
4. Download quality report metrics
5. Compile into presentation

---

## 🎮 Interactive Features

### Plots
- **Hover** → See exact values
- **Click legend** → Toggle device visibility
- **Zoom** → Drag to zoom in
- **Pan** → Click+drag on plot
- **Home** → Reset zoom/pan

### Tables
- **Sort** → Click column header
- **Search** → Use browser Ctrl+F
- **Pagination** → Navigate pages

### Dropdowns
- **Multi-select** → Click multiple devices
- **Select All** → Often available at top

---

## 💡 Tips & Tricks

1. **Start with "Show all measurement points"** to understand data distribution
2. **Use recommended filter ranges** as starting point
3. **Export raw data first** before applying aggressive filters
4. **Check "By Day" view** to spot problematic measurement days
5. **Compare before/after filtering** in quality report

---

## 🔧 Common Settings

### Conservative Filtering (Keep more data)
```
PCE:  5% to 30%
Jsc:  10 to 50
Voc:  0.4 to 1.6
FF:   40 to 90
```

### Aggressive Filtering (Remove outliers)
```
PCE:  10% to 25%
Jsc:  25 to 45
Voc:  0.8 to 1.2
FF:   60 to 85
```

### No Filtering (Keep all data)
- Click "❌ Clear Filters" button

---

## 📝 File Format Requirements

Your .txt files should contain data like this:
```
Scan  Jsc(mA/cm²)  Voc(V)  FF(%)  PCE(%)
1     42.3         0.92    78.5   30.5
2     41.8         0.91    79.2   30.1
3     43.1         0.93    77.8   31.2
```

**Filename must be:**
`prefix_Stability (JV)_Stability-D<day>-<device>-<pixel>.txt`

**Example:**
`0001_2026-03-28_13.59.47_Stability (JV)_Stability-D14-40-1A.txt`

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| No files detected | Check filename format, use Upload option |
| Missing columns | Verify file has Jsc, Voc, FF, PCE columns |
| No data in tables | Upload files, don't just specify folder |
| Filters not working | Use number inputs (not text), min < max |
| Plots look empty | Check device selection, apply Tab 3 filters |
| Slow to load | Apply filters in Tab 3 to reduce data |

---

## 🎓 Learning Path

**Beginner (10 min)**
1. Load sample data
2. View Tab 2 (Raw Data)
3. View Tab 1 (Analysis)

**Intermediate (20 min)**
1. Complete Beginner steps
2. Try filtering in Tab 3
3. View Tab 4 (Statistics)
4. Export CSV

**Advanced (30+ min)**
1. Complete Intermediate steps
2. Analyze multiple devices
3. Compare before/after filtering
4. Use Python/Excel for CSV analysis

---

## 📞 Getting Help

1. **Check Tab 2** → Raw Data exists?
2. **Check Tab 3** → Statistics reasonable?
3. **Try clearing filters** → Does data reappear?
4. **Re-upload files** → Try fresh data load
5. **Check file format** → Matches requirements?

---

## ✨ Next Steps

- ✅ Explore all tabs with your data
- ✅ Try different filter ranges
- ✅ Export CSV files for external analysis
- ✅ Compare multiple devices
- ✅ Share results with team

**Happy analyzing!** 🔬📊✨

---

*For more details, see README.md and IMPLEMENTATION_SUMMARY.md*
