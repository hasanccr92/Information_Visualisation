import csv
import sys
import os
from collections import Counter, defaultdict


def _here(*parts):
    """
    Build a path relative to this script's directory.
    This makes the script work whether it's run from the project root
    or from inside the data directory.
    """
    return os.path.join(os.path.dirname(__file__), *parts)


def diagnose_tsv(filename, sample_size=10):
    print(f"\n{'='*80}")
    print(f"DIAGNOSING: {filename}")
    print(f"{'='*80}\n")
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        # Get column names
        fieldnames = reader.fieldnames
        print(f"COLUMNS ({len(fieldnames)}):")
        for i, col in enumerate(fieldnames, 1):
            print(f"  {i}. '{col}'")
        
        print(f"\n{'='*80}")
        print(f"SAMPLE ROWS (first {sample_size}):")
        print(f"{'='*80}\n")
        
        rows = []
        for i, row in enumerate(reader):
            rows.append(row)
            if i < sample_size:
                print(f"Row {i+1}:")
                for col in fieldnames:
                    value = row[col]
                    print(f"  {col}: '{value}'")
                print()
            if i >= 10000:  # Limit for performance
                break
        
        return fieldnames, rows

def analyze_players(filename):
    print(f"\n{'='*80}")
    print(f"ANALYZING PLAYERS: {filename}")
    print(f"{'='*80}\n")
    
    sex_counter = Counter()
    birthyear_sample = []
    max_rating_sample = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        for i, row in enumerate(reader):
            # Count sex values
            sex = row.get('sex', '').strip()
            sex_counter[sex] += 1
            
            # Sample birthyears
            if i < 20:
                birthyear_sample.append(row.get('birthyear', ''))
            
            # Sample max_rating
            if i < 20:
                max_rating_sample.append(row.get('max_rating', ''))
    
    print("SEX DISTRIBUTION:")
    for sex, count in sex_counter.most_common():
        print(f"  '{sex}': {count:,}")
    
    print(f"\nBIRTHYEAR SAMPLES (first 20):")
    for i, by in enumerate(birthyear_sample, 1):
        print(f"  {i}. '{by}'")
    
    print(f"\nMAX_RATING SAMPLES (first 20):")
    for i, mr in enumerate(max_rating_sample, 1):
        print(f"  {i}. '{mr}'")

def analyze_ratings(filename):
    print(f"\n{'='*80}")
    print(f"ANALYZING RATINGS: {filename}")
    print(f"{'='*80}\n")
    
    month_counter = Counter()
    rating_ranges = defaultdict(int)
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        sample_months = set()
        
        for i, row in enumerate(reader):
            month = row.get('month', '').strip()
            rating = row.get('rating', '').strip()
            
            if i < 20:
                sample_months.add(month)
            
            if month:
                month_counter[month[:4]] += 1  # Count by year
            
            try:
                r = int(rating) if rating else 0
                if r > 0:
                    if r < 1500:
                        rating_ranges['<1500'] += 1
                    elif r < 2000:
                        rating_ranges['1500-2000'] += 1
                    elif r < 2400:
                        rating_ranges['2000-2400'] += 1
                    elif r < 2600:
                        rating_ranges['2400-2600'] += 1
                    else:
                        rating_ranges['2600+'] += 1
            except:
                pass
            
            if i >= 100000:  # Limit for performance
                break
    
    print("SAMPLE MONTHS (first 20 unique):")
    for month in sorted(sample_months)[:20]:
        print(f"  '{month}'")
    
    print(f"\nRATINGS BY YEAR (first 10 years):")
    for year, count in sorted(month_counter.items())[:10]:
        print(f"  {year}: {count:,}")
    
    print(f"\nRATING RANGES (from first 100k records):")
    for range_name, count in sorted(rating_ranges.items()):
        print(f"  {range_name}: {count:,}")

def cross_reference(players_file, ratings_file):
    print(f"\n{'='*80}")
    print(f"CROSS-REFERENCING PLAYERS AND RATINGS")
    print(f"{'='*80}\n")
    
    # Load player sex mapping
    player_sex = {}
    female_ids = []
    male_ids = []
    
    with open(players_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for i, row in enumerate(reader):
            # In these TSVs the id column is named '#id'
            player_id = row.get('#id', '').strip()
            sex = row.get('sex', '').strip()
            if player_id:
                player_sex[player_id] = sex
                if sex == 'F':
                    female_ids.append(player_id)
                    if len(female_ids) <= 10:
                        print(f"Female player ID sample: {player_id}, Name: {row.get('name', '')}")
                elif sex == 'M':
                    male_ids.append(player_id)
    
    print(f"\nTotal players: {len(player_sex):,}")
    print(f"Female players: {len(female_ids):,}")
    print(f"Male players: {len(male_ids):,}")
    
    # Check if female IDs exist in ratings
    print(f"\nChecking first 10 female player IDs in ratings file...")
    
    female_rating_count = 0
    male_rating_count = 0
    
    with open(ratings_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        for i, row in enumerate(reader):
            # Ratings TSV also uses '#id' for the player identifier
            player_id = row.get('#id', '').strip()
            
            if player_id in player_sex:
                sex = player_sex[player_id]
                if sex == 'F':
                    female_rating_count += 1
                    if female_rating_count <= 5:
                        print(f"  Found female rating: ID={player_id}, month={row.get('month')}, rating={row.get('rating')}")
                elif sex == 'M':
                    male_rating_count += 1
            
            if i >= 100000:  # Limit
                break
    
    print(f"\nRatings found (first 100k records):")
    print(f"  Female ratings: {female_rating_count:,}")
    print(f"  Male ratings: {male_rating_count:,}")

if __name__ == "__main__":
    # Use paths relative to this script so it works no matter the CWD
    players_path = _here("players-medium.tsv")
    ratings_path = _here("ratings-medium.tsv")

    # Diagnose players-medium
    fieldnames_players, rows_players = diagnose_tsv(players_path, sample_size=5)

    # Diagnose ratings-medium
    fieldnames_ratings, rows_ratings = diagnose_tsv(ratings_path, sample_size=5)

    # Analyze players
    analyze_players(players_path)

    # Analyze ratings
    analyze_ratings(ratings_path)

    # Cross-reference
    cross_reference(players_path, ratings_path)

    print(f"\n{'='*80}")
    print("DIAGNOSIS COMPLETE")
    print(f"{'='*80}\n")