# CSV-BETO

CSV-BETO is a comprehensive data analysis tool that fetches comments data from JSONPlaceholder API, processes it with pandas, performs statistical analysis, creates visualizations with matplotlib, and exports results to CSV format.

## Features

- **API Data Fetching**: Retrieves 500+ comment records from jsonplaceholder.typicode.com/comments
- **Data Processing**: Uses pandas for data transformation and enrichment
- **Statistical Analysis**: Calculates various metrics including:
  - Average comments per week
  - Word count statistics
  - User activity patterns
  - Email domain analysis
- **Data Visualization**: Creates multiple plots using matplotlib and seaborn:
  - Time series of comments per week
  - Word count distributions
  - User activity patterns
  - Correlation matrices
- **CSV Export**: Saves all processed data and statistics to CSV files
- **Robust Design**: Includes fallback to mock data when API is unavailable

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CSV-BETO
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main analysis script:
```bash
python3 comments_analysis.py
```

The script will:
1. Attempt to fetch data from JSONPlaceholder API
2. If API is unavailable, generate mock data for demonstration
3. Process the data with pandas
4. Calculate comprehensive statistics
5. Generate visualizations
6. Export results to CSV files

## Generated Files

After running the analysis, the following files will be created:

### CSV Files
- `comments_processed_data.csv` - Complete processed dataset with all features
- `weekly_statistics.csv` - Weekly aggregated statistics
- `summary_statistics.csv` - Key summary metrics

### Visualizations
- `comments_analysis_dashboard.png` - Multi-panel dashboard with 6 different plots
- `weekly_trend_analysis.png` - Detailed weekly trend analysis

## Data Analysis Features

### Statistical Metrics
- **Total Comments**: Complete count of analyzed comments
- **Weekly Analysis**: Average, median, and standard deviation of comments per week
- **Text Analysis**: Word count statistics and comment length analysis
- **User Patterns**: User activity and posting frequency analysis
- **Domain Analysis**: Email domain distribution analysis

### Visualizations
1. **Time Series Plot**: Comments volume over time with average line
2. **Word Count Distribution**: Histogram of comment word counts
3. **Top Email Domains**: Bar chart of most common email domains
4. **Comment Length by Category**: Average length analysis by text categories
5. **User Activity Distribution**: User posting frequency patterns
6. **Correlation Matrix**: Feature correlation heatmap

## Technical Implementation

### Libraries Used
- **requests**: For API data fetching
- **pandas**: For data processing and analysis
- **matplotlib**: For plotting and visualization
- **seaborn**: For enhanced statistical visualizations
- **numpy**: For numerical computations
- **scipy**: For advanced statistical analysis

### Data Processing Pipeline
1. **Data Fetching**: API call with fallback to mock data
2. **Data Enrichment**: Addition of synthetic dates, word counts, and user statistics
3. **Feature Engineering**: Creation of derived features like email domains and text categories
4. **Statistical Analysis**: Comprehensive statistical computations
5. **Visualization**: Multiple plot generation with matplotlib/seaborn
6. **Export**: CSV file generation for all results

## Mock Data
When the JSONPlaceholder API is unavailable, the tool generates realistic mock data that maintains the same structure and statistical properties, ensuring the analysis pipeline can always be demonstrated.

## Example Output

```
=== Key Statistics ===
Total Comments: 500
Average Comments per Week: 45.45
Median Comments per Week: 49.00
Standard Deviation: 12.14
Average Word Count: 21.52
Median Word Count: 21.00
```

## Requirements
- Python 3.7+
- Internet connection (optional - fallback to mock data available)
- See `requirements.txt` for complete dependency list