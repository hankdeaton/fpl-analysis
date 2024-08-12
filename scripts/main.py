import fpl_functions

dp_df = fpl_functions.create_draft_rankings("../data/fantrax_player_proj_24_25.csv")

dp_df.to_csv("../data/draft_rankings.csv")