import nflreadpy as nfl
import pandas as pd

def get_latest_player_stats(season=2026):
    print(f"Fetching player stats for the {season} season...")
    weekly_stats = nfl.load_player_stats([season])

    if hasattr(weekly_stats, "to_pandas"):
        df = weekly_stats.to_pandas()
    else:
        df = weekly_stats
    return df

def calculate_dynasty_indicators(weekly_df):
    if weekly_df.empty:
        print("No data available for this season yet.")
        return pd.DataFrame()

    reg_season = weekly_df[weekly_df['season_type'] == 'REG']
    if reg_season.empty:
        return pd.DataFrame()

    summary = reg_season.groupby(['player_id', 'player_name', 'position']).agg(
        games_played=('week', 'count'),
        avg_targets=('targets', 'mean'),
        avg_fantasy_points=('fantasy_points_ppr', 'mean')
    ).reset_index()

    return summary

def generate_buy_low_sell_high(summary_df):
    print("\n--- DYNASTY TARGET REPORT ---")
    if summary_df.empty:
        print("Not enough regular season data to generate insights yet.")
        return

    buy_lows = summary_df[(summary_df['avg_targets'] > 6.0) & (summary_df['avg_fantasy_points'] < 12.0)]

    print("Potential Buy-Low Candidates (High Target Volume, Lower Fantasy Output):")
    for _, row in buy_lows.iterrows():
        print(f"- {row['player_name']} ({row['position']}): {row['avg_targets']:.1f} targets/gm, {row['avg_fantasy_points']:.1f} PPR pts/gm")

if __name__ == "__main__":
    df = get_latest_player_stats()
    summary = calculate_dynasty_indicators(df)
    generate_buy_low_sell_high(summary)
