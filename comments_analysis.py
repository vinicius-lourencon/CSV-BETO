#!/usr/bin/env python3
"""
CSV-BETO: Comments Data Analysis
Fetches comments from JSONPlaceholder API, analyzes data with pandas,
creates visualizations with matplotlib, and exports to CSV.
"""

import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environment
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import random
import re
from typing import Dict, List
import statistics

class CommentsAnalyzer:
    def __init__(self):
        self.api_url = "https://jsonplaceholder.typicode.com/comments"
        self.data = None
        self.processed_data = None
        
    def fetch_comments(self) -> pd.DataFrame:
        """
        Fetch comments data from JSONPlaceholder API with fallback to mock data
        """
        print("Fetching comments from JSONPlaceholder API...")
        
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            comments_data = response.json()
            print(f"Successfully fetched {len(comments_data)} comments from API")
            
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            print("Using mock data for demonstration...")
            comments_data = self._generate_mock_data()
            
        # Convert to DataFrame
        df = pd.DataFrame(comments_data)
        
        # Add synthetic date column for week analysis (since API doesn't provide dates)
        # Generate random dates over the past 10 weeks for demonstration
        start_date = datetime.now() - timedelta(weeks=10)
        dates = []
        for _ in range(len(df)):
            random_days = random.randint(0, 70)  # 10 weeks = 70 days
            date = start_date + timedelta(days=random_days)
            dates.append(date)
        
        df['date'] = dates
        df['week'] = df['date'].dt.isocalendar().week
        df['year_week'] = df['date'].dt.strftime('%Y-W%U')
        
        # Add word count for additional analysis
        df['word_count'] = df['body'].apply(lambda x: len(x.split()))
        
        self.data = df
        return df
    
    def _generate_mock_data(self) -> List[Dict]:
        """
        Generate mock comments data that mimics JSONPlaceholder structure
        """
        print("Generating 500+ mock comments for demonstration...")
        
        mock_comments = []
        sample_bodies = [
            "laudantium enim quasi est quidem magnam voluptate ipsam eos tempora quo necessitatibus dolor quam autem quasi reiciendis et nam sapiente accusantium",
            "est natus enim nihil est dolore omnis voluptatem numquam et omnis occaecati quod ullam at voluptatem error expedita pariatur nihil sint nostrum voluptatem",
            "quia molestiae reprehenderit quasi aspernatur aut expedita occaecati aliquam eveniet laudantium omnis quibusdam delectus saepe quia accusamus maiores nam est",
            "non et atque occaecati deserunt quas accusantium unde odit nobis qui voluptatem quia voluptas consequuntur itaque dolor et qui rerum deleniti ut occaecati",
            "harum non quasi et ratione tempore iure ex voluptates in ratione harum architecto fugit inventore cupiditate voluptates magni quo et",
            "doloribus at sed quis culpa deserunt consectetur qui praesentium accusamus fugiat dicta voluptatem rerum ut voluptate autem voluptatem repellendus aspernatur",
            "maiores sed dolores similique labore et inventore et quasi temporibus esse sunt id et eos voluptatem aliquam aliquid ratione corporis molestiae mollitia quia",
            "ut voluptatem corrupti velit ad voluptatem maiores et nisi velit vero accusamus maiores voluptates sequi et unde sed ut sed aliquam",
            "sapiente assumenda molestiae atque adipisci laborum distinctio aperiam et ab ut omnis et occaecati aspernatur odit sit rem expedita quas enim",
            "voluptate iusto quis nobis reprehenderit ipsum amet nulla quia quas dolores velit et non aut quia necessitatibus nostrum quaerat nulla et accusamus nisi facilis"
        ]
        
        sample_names = [
            "Eliseo", "Jayne_Kuhic", "Nikita", "Lew", "Hayden", "Presley.Mueller", "Dallas", "Mallory_Kunze", "Meghan_Littel", "Carmen_Keeling"
        ]
        
        sample_emails = [
            "Eliseo@gardner.biz", "Jayne_Kuhic@sydney.com", "Nikita@garfield.biz", "Lew@alysha.tv", "Hayden@althea.biz",
            "Presley.Mueller@myrl.com", "Dallas@ole.me", "Mallory_Kunze@marie.org", "Meghan_Littel@rosamond.me", "Carmen_Keeling@caroline.name"
        ]
        
        # Generate 500+ comments
        for i in range(500):
            comment = {
                "postId": random.randint(1, 100),
                "id": i + 1,
                "name": random.choice(sample_names),
                "email": random.choice(sample_emails),
                "body": random.choice(sample_bodies)
            }
            mock_comments.append(comment)
        
        print(f"Generated {len(mock_comments)} mock comments")
        return mock_comments
    
    def process_data(self) -> pd.DataFrame:
        """
        Process and transform data using pandas
        """
        if self.data is None:
            raise ValueError("No data available. Please fetch data first.")
        
        print("Processing data with pandas...")
        
        # Create processed dataset
        df = self.data.copy()
        
        # Clean email domains
        df['email_domain'] = df['email'].apply(lambda x: x.split('@')[1] if '@' in x else 'unknown')
        
        # Text length categories
        df['text_length_category'] = pd.cut(
            df['body'].str.len(), 
            bins=[0, 50, 100, 200, float('inf')], 
            labels=['Short', 'Medium', 'Long', 'Very Long']
        )
        
        # User posting frequency
        user_stats = df.groupby('email').agg({
            'id': 'count',
            'word_count': 'mean',
            'body': lambda x: x.str.len().mean()
        }).rename(columns={'id': 'post_count', 'word_count': 'avg_word_count', 'body': 'avg_length'})
        
        df = df.merge(user_stats, left_on='email', right_index=True, suffixes=('', '_user'))
        
        self.processed_data = df
        return df
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate various statistics from the data
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please process data first.")
        
        print("Calculating statistics...")
        
        df = self.processed_data
        
        stats = {
            'total_comments': len(df),
            'unique_users': df['email'].nunique(),
            'unique_posts': df['postId'].nunique(),
            'avg_comments_per_week': df.groupby('year_week').size().mean(),
            'median_comments_per_week': df.groupby('year_week').size().median(),
            'std_comments_per_week': df.groupby('year_week').size().std(),
            'avg_word_count': df['word_count'].mean(),
            'median_word_count': df['word_count'].median(),
            'avg_comment_length': df['body'].str.len().mean(),
            'median_comment_length': df['body'].str.len().median(),
            'top_email_domains': df['email_domain'].value_counts().head(5).to_dict(),
            'comments_by_week': df.groupby('year_week').size().to_dict(),
            'word_count_by_length_category': df.groupby('text_length_category')['word_count'].mean().to_dict()
        }
        
        print(f"Statistics calculated:")
        print(f"- Total comments: {stats['total_comments']}")
        print(f"- Average comments per week: {stats['avg_comments_per_week']:.2f}")
        print(f"- Average word count: {stats['avg_word_count']:.2f}")
        
        return stats
    
    def create_visualizations(self, stats: Dict):
        """
        Create various plots using matplotlib and seaborn
        """
        print("Creating visualizations...")
        
        df = self.processed_data
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Comments Data Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Comments per week (time series)
        weekly_data = df.groupby('year_week').size().sort_index()
        axes[0, 0].plot(range(len(weekly_data)), weekly_data.values, marker='o', linewidth=2)
        axes[0, 0].set_title('Comments per Week')
        axes[0, 0].set_xlabel('Week')
        axes[0, 0].set_ylabel('Number of Comments')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add average line
        avg_line = stats['avg_comments_per_week']
        axes[0, 0].axhline(y=avg_line, color='red', linestyle='--', 
                          label=f'Average: {avg_line:.1f}')
        axes[0, 0].legend()
        
        # 2. Word count distribution
        axes[0, 1].hist(df['word_count'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 1].set_title('Word Count Distribution')
        axes[0, 1].set_xlabel('Word Count')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].axvline(stats['avg_word_count'], color='red', linestyle='--', 
                          label=f'Mean: {stats["avg_word_count"]:.1f}')
        axes[0, 1].legend()
        
        # 3. Top email domains
        domains = list(stats['top_email_domains'].keys())[:5]
        counts = list(stats['top_email_domains'].values())[:5]
        axes[0, 2].bar(domains, counts, color='lightcoral')
        axes[0, 2].set_title('Top 5 Email Domains')
        axes[0, 2].set_xlabel('Domain')
        axes[0, 2].set_ylabel('Count')
        axes[0, 2].tick_params(axis='x', rotation=45)
        
        # 4. Comment length by category
        category_data = df.groupby('text_length_category')['body'].apply(lambda x: x.str.len().mean())
        axes[1, 0].bar(category_data.index, category_data.values, color='lightgreen')
        axes[1, 0].set_title('Average Comment Length by Category')
        axes[1, 0].set_xlabel('Length Category')
        axes[1, 0].set_ylabel('Average Characters')
        
        # 5. User activity distribution
        user_activity = df['post_count'].value_counts().head(10)
        axes[1, 1].bar(range(len(user_activity)), user_activity.values, color='orange')
        axes[1, 1].set_title('User Activity Distribution')
        axes[1, 1].set_xlabel('Comments per User')
        axes[1, 1].set_ylabel('Number of Users')
        
        # 6. Correlation heatmap
        numeric_cols = ['word_count', 'post_count', 'avg_word_count', 'avg_length']
        correlation_matrix = df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[1, 2])
        axes[1, 2].set_title('Feature Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig('/home/runner/work/CSV-BETO/CSV-BETO/comments_analysis_dashboard.png', 
                   dpi=300, bbox_inches='tight')
        print("Dashboard plot saved to: comments_analysis_dashboard.png")
        plt.close()
        
        # Create additional individual plots
        self._create_additional_plots(df, stats)
    
    def _create_additional_plots(self, df: pd.DataFrame, stats: Dict):
        """
        Create additional specialized plots
        """
        # Weekly trend analysis
        plt.figure(figsize=(12, 6))
        weekly_data = df.groupby('year_week').agg({
            'id': 'count',
            'word_count': 'mean'
        }).rename(columns={'id': 'comment_count'})
        
        # Dual axis plot
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        color = 'tab:blue'
        ax1.set_xlabel('Week')
        ax1.set_ylabel('Number of Comments', color=color)
        bars = ax1.bar(range(len(weekly_data)), weekly_data['comment_count'], 
                      color=color, alpha=0.7, label='Comments Count')
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Average Word Count', color=color)
        line = ax2.plot(range(len(weekly_data)), weekly_data['word_count'], 
                       color=color, marker='o', linewidth=2, label='Avg Word Count')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title('Weekly Comments Volume vs Average Word Count')
        fig.tight_layout()
        plt.savefig('/home/runner/work/CSV-BETO/CSV-BETO/weekly_trend_analysis.png', 
                   dpi=300, bbox_inches='tight')
        print("Weekly trend plot saved to: weekly_trend_analysis.png")
        plt.close()
    
    def export_to_csv(self):
        """
        Export processed data and statistics to CSV files
        """
        print("Exporting data to CSV files...")
        
        if self.processed_data is None:
            raise ValueError("No processed data available.")
        
        # Export main dataset
        csv_path = '/home/runner/work/CSV-BETO/CSV-BETO/comments_processed_data.csv'
        self.processed_data.to_csv(csv_path, index=False)
        print(f"Processed data exported to: {csv_path}")
        
        # Export weekly statistics
        weekly_stats = self.processed_data.groupby('year_week').agg({
            'id': 'count',
            'word_count': ['mean', 'median', 'std'],
            'body': lambda x: x.str.len().mean()
        }).round(2)
        
        weekly_stats.columns = ['comment_count', 'avg_word_count', 'median_word_count', 
                               'std_word_count', 'avg_comment_length']
        weekly_stats_path = '/home/runner/work/CSV-BETO/CSV-BETO/weekly_statistics.csv'
        weekly_stats.to_csv(weekly_stats_path)
        print(f"Weekly statistics exported to: {weekly_stats_path}")
        
        # Export summary statistics
        stats = self.calculate_statistics()
        summary_stats = []
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                summary_stats.append({'metric': key, 'value': value})
        
        summary_df = pd.DataFrame(summary_stats)
        summary_path = '/home/runner/work/CSV-BETO/CSV-BETO/summary_statistics.csv'
        summary_df.to_csv(summary_path, index=False)
        print(f"Summary statistics exported to: {summary_path}")
        
        return csv_path, weekly_stats_path, summary_path

def main():
    """
    Main function to run the complete analysis pipeline
    """
    print("=== CSV-BETO Comments Analysis Pipeline ===")
    print("This script will:")
    print("1. Fetch 500+ comments from JSONPlaceholder API")
    print("2. Process data with pandas")
    print("3. Calculate various statistics")
    print("4. Create visualizations with matplotlib")
    print("5. Export results to CSV files")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = CommentsAnalyzer()
    
    try:
        # Step 1: Fetch data
        df = analyzer.fetch_comments()
        print(f"\n✓ Successfully fetched {len(df)} comments")
        
        # Step 2: Process data
        processed_df = analyzer.process_data()
        print(f"✓ Data processed successfully")
        
        # Step 3: Calculate statistics
        stats = analyzer.calculate_statistics()
        print("✓ Statistics calculated")
        
        # Step 4: Create visualizations
        analyzer.create_visualizations(stats)
        print("✓ Visualizations created")
        
        # Step 5: Export to CSV
        csv_files = analyzer.export_to_csv()
        print("✓ Data exported to CSV files")
        
        print("\n=== Analysis Complete ===")
        print("Generated files:")
        for file_path in csv_files:
            print(f"- {file_path}")
        print("- comments_analysis_dashboard.png")
        print("- weekly_trend_analysis.png")
        
        # Print key statistics
        print(f"\n=== Key Statistics ===")
        print(f"Total Comments: {stats['total_comments']}")
        print(f"Average Comments per Week: {stats['avg_comments_per_week']:.2f}")
        print(f"Median Comments per Week: {stats['median_comments_per_week']:.2f}")
        print(f"Standard Deviation: {stats['std_comments_per_week']:.2f}")
        print(f"Average Word Count: {stats['avg_word_count']:.2f}")
        print(f"Median Word Count: {stats['median_word_count']:.2f}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        raise

if __name__ == "__main__":
    main()