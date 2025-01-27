import openai
import pandas as pd
from tqdm import tqdm



# Load the dataset
df = pd.read_pickle("2024_11_06_2246_articles_database.pkl")  # Replace with the path to your dataset
df = df[df['Title'].str.contains('Trump') | df['Title'].str.contains('Harris') | df['Title'].str.contains('Kamala')]
df = df.reset_index(drop=True)
#print(df)
headlines = df["Title"].tolist()  # Assuming the column with headlines is named 'headline'
#print(len(headlines))
#print(headlines)



# Function to analyze bias in a headline using the Chat Completion API
def analyze_bias_chat_api(headline):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(  # Updated method name
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant trained to analyze news headlines for bias."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze the following news headline and determine its stance toward Candidate Kamala Harris and Candidate Donald Trump in
                    the 2024 election. Classify the stance as positive, negative, neutral, or not mentioned for each candidate.
                    - Positive stance: Indicates support or favorable opinion.
                    - Negative stance: Indicates criticism or unfavorable opinion.
                    - Neutral stance: Indicates neither positive nor negative sentiment.
                    - Not mentioned: The candidate is not referenced in the headline.
                    
                    Here are a few examples:

                    Example 1:
                    Headline: "Kamala Harris proposes new healthcare plan praised by experts"
                    Stance toward Kamala Harris: positive
                    Stance toward Donald Trump: not mentioned

                    Example 2:
                    Headline: "Donald Trump criticized for remarks on international trade policies"
                    Stance toward Kamala Harris: not mentioned
                    Stance toward Donald Trump: negative

                    Example 3:
                    Headline: "Both Kamala Harris and Donald Trump attend 9/11 memorial"
                    Stance toward Kamala Harris: neutral
                    Stance toward Donald Trump: neutral

                    Now analyze the following:

                    Headline: "{headline}"
                    
                    Output format:
                    Stance toward Kamala Harris: <positive/negative/neutral/not mentioned>
                    
                    Stance toward Donald Trump: <positive/negative/neutral/not mentioned>
                    """
                }
            ]
        )
        return response.choices[0].message.content.strip()  # Keep this dictionary access for backward compatibility
    except Exception as e:
        return f"Error: {str(e)}"
# Process headlines in batches of 100

batch_size = 100
results = []

for i in tqdm(range(0, len(headlines), batch_size)):
    batch = headlines[i:i + batch_size]
    batch_results = [analyze_bias_chat_api(headline) for headline in batch]
    #print(batch_results)
    results.extend(batch_results)
    
    # Save interim results to a pickle file
    df.loc[i:i + batch_size - 1, "bias_analysis"] = batch_results
    df.iloc[i:i + batch_size].to_pickle(f"batch_results_gpt-4o-mini_fewshot{i // batch_size}.pkl")

# Save the full dataset with results
df.to_pickle("full_results_with_bias_analysis_gpt-4o-mini_fewshot.pkl")
