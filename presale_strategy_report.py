# -*- coding: utf-8 -*-
"""Presale Strategy Report-30/1/25

# Install
"""

import openai
import json
import re
from dotenv import load_dotenv
import time
import asyncio
import nest_asyncio

from pydantic import BaseModel, Field, ConfigDict
from typing import List
from openai import OpenAI

load_dotenv()
# Install necessary libraries
# !pip install openai
# !pip install fpdf
# !pip install nest_asyncio

"""# **Presale Report Model**

## Liberaries
"""

# import Lib's


# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
# Replace 'your-openai-api-key' with your actual OpenAI API key
# Set up environment and API key

"""## Class"""

##Structure format Classes

client = OpenAI()


class Key_Takeaways(BaseModel):
    Online_Ratings: str = Field(alias="Online Ratings")
    Major_Pain_Points: str = Field(alias="Major Pain Points")
    Opportunities: str = Field(alias="Opportunities")
    Action_Steps: str = Field(alias="Action Steps")
    Projected_Impact: str = Field(alias="Projected Impact")

    model_config = ConfigDict(populate_by_name=True)


class Executive_Summary(BaseModel):
    Overall_Summary: str = Field(alias="Overall Summary")
    Key_Takeaway: Key_Takeaways = Field(alias="Key Takeaways")

    model_config = ConfigDict(populate_by_name=True)


class Business_Overview(BaseModel):
    content: str
    Primary_Services: str = Field(alias="Primary Services")
    Market_Position: str = Field(alias="Market Position")
    Unique_Selling_Proposition: str = Field(alias="Unique Selling Proposition")

    model_config = ConfigDict(populate_by_name=True)


class SWOT(BaseModel):
    Strengths: List[str]
    Weaknesses: List[str]
    Opportunities: List[str]
    Threats: List[str]

    model_config = ConfigDict(populate_by_name=True)


class Key_Positive_Driver(BaseModel):
    Name: str
    Impact: str
    Recommendation: str

    model_config = ConfigDict(populate_by_name=True)


class Key_Negative_Driver(BaseModel):
    Name: str
    Impact: str
    Recommendation: str

    model_config = ConfigDict(populate_by_name=True)


class CustomerSentimentKeyDrivers(BaseModel):
    Total_Text_Reviews_Analyzed: int
    Positive: float
    Neutral: float
    Negative: float
    Key_Positive_Drivers: List[Key_Positive_Driver]
    Key_Negative_Drivers: List[Key_Negative_Driver]

    Google: str = Field(alias="Google: Rating: ")

    model_config = ConfigDict(populate_by_name=True)


class table(BaseModel):
    Company: str
    Avg_Rating: float
    Core_Differentiator: str

    model_config = ConfigDict(populate_by_name=True)


class CompetitiveBenchmarking(BaseModel):
    table_section: List[table]
    Insights: List[str]

    model_config = ConfigDict(populate_by_name=True)


class Point_1(BaseModel):
    Heading: str
    Content_1: str
    Content_2: str

    model_config = ConfigDict(populate_by_name=True)


class ROIBusinessImpactProjections(BaseModel):
    point_1: List[Point_1]
    Point_2: List[Point_1]
    Point_3: List[Point_1]

    model_config = ConfigDict(populate_by_name=True)


class Report(BaseModel):
    Pre_Sales_Reputation_Analysis_Report: str = Field(
        alias="Pre-Sales Reputation Analysis Report"
    )
    Seller_Company_Name: str = Field(alias="Seller Company Name")
    Seller_Product_Details: str = Field(alias="Seller Product Details")
    Executive_Summary_Section: List[Executive_Summary] = Field(
        alias="1. Executive Summary"
    )
    Business_Overview_Section: List[Business_Overview] = Field(
        alias="2. Business Overview"
    )
    SWOT_section: list[SWOT] = Field(alias="3. SWOT Analysis")
    Customer_Sentiment_Key_Drivers_Section: List[CustomerSentimentKeyDrivers] = Field(
        alias="4. Customer Sentiment & Key Drivers"
    )
    Competitive_Benchmarking_Section: List[CompetitiveBenchmarking] = Field(
        alias="5. Competitive Benchmarking"
    )
    Recommendations_Section: List[str] = Field(alias="6. Recommendations")
    ROI_Business_Impact_Projections_Section: List[ROIBusinessImpactProjections] = Field(
        alias="7. ROI / Business Impact Projections"
    )

    model_config = ConfigDict(populate_by_name=True)


class Pointers(BaseModel):
    pointer_heading: str
    first_point: str
    second_point: str


class SuggestedTargetAudience(BaseModel):
    suggested_target_audience: list[Pointers]


"""## Model"""


def extract_reviews(json_list_string):
    # Check if the input string is empty
    if not json_list_string.strip():
        return None

    # Remove the outer list brackets and split the string into components
    if json_list_string.startswith("[") and json_list_string.endswith("]"):
        json_list_string = json_list_string[1:-1].strip()

    # Split the string into individual dictionary-like components
    # Assuming the dictionaries are separated by '}, {'
    dict_strings = re.split(r"\},\s*\{", json_list_string)

    # Clean up each dictionary string
    dict_strings = [
        ("{" + d + "}")
        .replace("'", '"')
        .replace("None", "null")
        .replace("\\n", "\\\\n")
        for d in dict_strings
    ]

    # Parse each component as JSON and extract fields
    extracted_data = []
    for dict_str in dict_strings:
        try:
            item = json.loads(dict_str)
            extracted_data.append({
                "rating": item["rating"],
                "review": item["review"],
                "review_username": item["review_username"],
            })
        except json.JSONDecodeError as e:
            print(f"Error parsing dictionary string: {e}")

    return extracted_data if extracted_data else None


def All_extract_data(
    Reviews_local_and_social,
    Reviews_local_and_social_Comp_1,
    Reviews_local_and_social_Comp_2,
    Reviews_local_and_social_Comp_3,
):
    # Extract reviews and assign them back to the variable
    reviews = extract_reviews(Reviews_local_and_social)
    if reviews is not None:
        Reviews_local_and_social = str(reviews)
    else:
        Reviews_local_and_social = "No reviews could be parsed or variable was empty"

    reviews = extract_reviews(Reviews_local_and_social_Comp_1)
    if reviews is not None:
        Reviews_local_and_social_Comp_1 = str(reviews)
    else:
        Reviews_local_and_social_Comp_1 = (
            "No reviews could be parsed or variable was empty"
        )

    reviews = extract_reviews(Reviews_local_and_social_Comp_2)
    if reviews is not None:
        Reviews_local_and_social_Comp_2 = str(reviews)
    else:
        Reviews_local_and_social_Comp_2 = (
            "No reviews could be parsed or variable was empty"
        )

    reviews = extract_reviews(Reviews_local_and_social_Comp_3)
    if reviews is not None:
        Reviews_local_and_social_Comp_3 = str(reviews)
    else:
        Reviews_local_and_social_Comp_3 = (
            "No reviews could be parsed or variable was empty"
        )

    return (
        Reviews_local_and_social,
        Reviews_local_and_social_Comp_1,
        Reviews_local_and_social_Comp_2,
        Reviews_local_and_social_Comp_3,
    )


async def fetch_openai_response(
    prompt, model="gpt-4.1", max_tokens=1500, temperature=0.3
):
    start_time = time.time()

    # Run the blocking OpenAI API call in a thread
    response = await asyncio.to_thread(
        openai.chat.completions.create,
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a professional digital marketing consultant.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    end_time = time.time()  # End the timer

    execution_time = end_time - start_time
    print(f"Execution section time: {execution_time:.6f} seconds")

    return response.choices[0].message.content


async def website_cleaning(website_content):
    start_time = time.time()  # Start the timer

    if len(website_content) > 0:
        website_cleaning = (
            """//Remove any redundancies and duplicates from the provided website content.
                        //Follow the below instructions:
                          1.Fix minor grammar issues, typos, capitalizations, and punctuation.
                          2.Maintain the original point of view (POV), voice, and tone without alteration.
                          3.Exclude unwanted elements are not part of the main content:
                            a.CTAs (Call to Action elements)
                            b.Advertisements
                            c.Social media sharing buttons
                            d.Hyperlinks
                            e.Navigation menus
                            f.Comments sections"""
            + """
      //Summarise the above website content based on the following heads-
      1. Core Business & Brand Identity
      Company Overview: Who they are, their history, or founding story (if prominently mentioned).
     Mission & Vision: The broader purpose and goals stated on the site.
      Brand Voice or Tone: Formal, casual, or conversational?
    2. Product & Service Offerings
        Primary Services/Products: A concise list of what they sell or do, emphasizing the most frequently mentioned or featured.
        Key Features or Benefits: What the site highlights as the biggest selling points or differentiators (e.g., “eco-friendly,” “24/7 support,” etc.).
        Special Packages or Bundles: Any promotions, tiered pricing, or unique offerings.
    3. Unique Selling Proposition (USP)
          What Sets Them Apart: Any claims about why they’re better/different than competitors (e.g., “fastest in the market,” “award-winning,” “family-owned”).
          Customer-Focused Statements: If they emphasize “customer first,” “best customer service,” or similar angles.
    4. Target Audience & Industry Positioning
          Who They Cater To: Residential customers, small/medium businesses, enterprise clients, etc.
          Market or Industry: Any stated niche or vertical focus (e.g., “serving healthcare providers,” “specializing in HVAC repairs”).

    5. Approach to Customer Service
        Support Channels: Phone, email, live chat, or in-person.
          Service Guarantees: Satisfaction guaranteed, warranties, return policies, or money-back offers if stated.
    6. Social Proof & Trust Signals
        Testimonials or Reviews: Internal testimonials, star ratings, or client logos.
        Certifications/Awards: “BBB Accredited,” “Top Service Award,” “ISO Certified,” or any relevant badges.
          Partnerships: Associations with well-known brands or industry coalitions.
      """
            + website_content
        )

        # Run the blocking OpenAI API call in a thread
        completion = await asyncio.to_thread(
            openai.chat.completions.create,
            model="gpt-4.1",
            temperature=0.5,
            max_tokens=4096,
            messages=[{"role": "user", "content": website_cleaning}],
        )
        website_completion_text = completion.choices[0].message.content

        print("Website Summary:", website_completion_text)

    else:
        website_completion_text = website_content

    end_time = time.time()  # End the timer

    execution_time = end_time - start_time
    print(f"Execution Website time: {execution_time:.6f} seconds")

    return website_completion_text


async def generate_report_async(
    seller_company_name,
    seller_product_details,
    prospect_company_name,
    Website_URL,
    Website_Content_Scrapped,
    BB_Category_Primary,
    BB_Category_Secondary,
    All_Signals_Data,
    Reviews_local_and_social,
    Business_Name_Comp_1,
    Website_URL_Comp_1,
    Website_Content_Scrapped_Comp_1,
    Competitor_Signals_Comp_1,
    BB_Category_Primary_Comp_1,
    Reviews_local_and_social_Comp_1,
    BB_Category_Secondary_Comp_1,
    Business_Name_Comp_2,
    Website_URL_Comp_2,
    Website_Content_Scrapped_Comp_2,
    Competitor_Signals_Comp_2,
    BB_Category_Primary_Comp_2,
    Reviews_local_and_social_Comp_2,
    BB_Category_Secondary_Comp_2,
    Business_Name_Comp_3,
    Website_URL_Comp_3,
    Website_Content_Scrapped_Comp_3,
    Competitor_Signals_Comp_3,
    BB_Category_Primary_Comp_3,
    Reviews_local_and_social_Comp_3,
    BB_Category_Secondary_Comp_3,
) -> tuple[
    str,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
    str | None,
]:
    # Running website cleaning concurrently
    cleaned_contents = await asyncio.gather(
        website_cleaning(Website_Content_Scrapped),
        website_cleaning(Website_Content_Scrapped_Comp_1),
        website_cleaning(Website_Content_Scrapped_Comp_2),
        website_cleaning(Website_Content_Scrapped_Comp_3),
    )

    (
        Website_Content_Scrapped,
        Website_Content_Scrapped_Comp_1,
        Website_Content_Scrapped_Comp_2,
        Website_Content_Scrapped_Comp_3,
    ) = cleaned_contents

    (
        Reviews_local_and_social,
        Reviews_local_and_social_Comp_1,
        Reviews_local_and_social_Comp_2,
        Reviews_local_and_social_Comp_3,
    ) = All_extract_data(
        Reviews_local_and_social,
        Reviews_local_and_social_Comp_1,
        Reviews_local_and_social_Comp_2,
        Reviews_local_and_social_Comp_3,
    )

    print("Reviews_local_and_social", Reviews_local_and_social)
    print("Reviews_local_and_social_Comp_1", Reviews_local_and_social_Comp_1)
    # Define prompts
    Business_Overview_prompt = f"""Create a Business Overview:
    **Scenario:**
    - **Prospect Company Name:** {prospect_company_name}
    - **Website URL:** {Website_URL}
    - **Website Content Scrapped:** {Website_Content_Scrapped}
    - **Business Category Primary:** {BB_Category_Primary}
    - **Business Category Secondary:** {BB_Category_Secondary}
    - **All Signals Data:** {All_Signals_Data}

    Output format:
    Overview content:
    Primary Services: ,
    Market Position: ,
    Unique Selling Proposition:
    
    **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english. Please dont add a seperate section on this just make the overall output in understandle easy english
    """

    SWOT_Analysis_prompt = f"""
    Create a SWOT Analysis:
    **Scenario:**
    - **Prospect Company Name:** {prospect_company_name}
    - **Google & Social Reviews:** {Reviews_local_and_social}
    - **Category:** {BB_Category_Primary}, {BB_Category_Secondary}
    - **Competitor Reviews:**
      - **Comp 1:** {Reviews_local_and_social_Comp_1}
      - **Comp 2:** {Reviews_local_and_social_Comp_2}
      - **Comp 3:** {Reviews_local_and_social_Comp_3}
    - **All Signals Data:** {All_Signals_Data}



    Output format:**Strictly follow the Character Limit between 380 to 400 characters for each field**
    Strengths:
    Weaknesses:
    Opportunities:
    Threats:
    
    **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english

    """

    Customer_Sentiment_prompt = (
        f"""
    Analyze Customer Sentiment & Key Drivers:
    **Scenario:**
    - **Google Reviews:** {Reviews_local_and_social}
    """
        + "\n"
        + """Output format:
    {
    "Total Text Reviews Analyzed": "Total Text Reviews Analyzed",
    "Positive": "Positive",
    "Neutral": "Neutral",
    "Negative": "Negative",
    "Key Positive Drivers": {
        "Name": "Name",
        "Impact": "Impact",
        "Recommendation": "Recommendation"
    },
    "Key Negative Drivers": {
        "Name": "Name",
        "Impact": "Impact",
        "Recommendation": "Recommendation"
    },
    "Google: Rating: ": "Google: Rating: "
}

    **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english
    Also very importantly make sure 
    Key Positive Drivers - (character limit of 200 char)
    Key Negative Drivers - (character limit of 200 char)
    It should not break the character limit

    """
    )

    Competitive_Benchmarking_prompt = (
        f"""
    Conduct Competitive Benchmarking:
    **Scenario:**
    - **Business Name - Comp 1:** {Business_Name_Comp_1}
    - **Reviews (local and social) Comp 1:** {Reviews_local_and_social_Comp_1}
    - **Competitor Signals Comp 1:** {Competitor_Signals_Comp_1}
    - **BB Category - Primary & Secondary Comp 1:** {BB_Category_Primary_Comp_1}, {BB_Category_Secondary_Comp_1}
    - **Business Name - Comp 2:** {Business_Name_Comp_2}
    - **Reviews (local and social) Comp 2:** {Reviews_local_and_social_Comp_2}
    - **Competitor Signals Comp 2:** {Competitor_Signals_Comp_2}
    - **BB Category - Primary & Secondary Comp 2:** {BB_Category_Primary_Comp_2}, {BB_Category_Secondary_Comp_2}
    - **Business Name - Comp 3:** {Business_Name_Comp_3}
    - **Reviews (local and social) Comp 3:** {Reviews_local_and_social_Comp_3}
    - **Competitor Signals Comp 3:** {Competitor_Signals_Comp_3}
    - **BB Category - Primary & Secondary Comp 3:** {BB_Category_Primary_Comp_3}, {BB_Category_Secondary_Comp_3}
    """
        + "\n"
        + """
    Output format:
    Competitive Benchmarking": [
                          {
                              "table_section": [
                                  {
                                      "Company": "Company",
                                      "Avg_Rating": "Avg_Rating",
                                      "Core_Differentiator": "Core_Differentiator",

                                  },
                                  {
                                      "Company": "Company",
                                      "Avg_Rating": "Avg_Rating",
                                      "Core_Differentiator": "Core_Differentiator",

                                  },
                                  {
                                      "Company": "Company",
                                      "Avg_Rating": "Avg_Rating",
                                      "Core_Differentiator": "Core_Differentiator",

                                  }
                              ],

                              "Insights" : ["", "", ""]
                          }
                      ]
                      
    **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand.Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english
    """
    )

    ROI_Impact_Projections_prompt = (
        f"""
    Project ROI / Business Impact:
    **Scenario:**
    - **Reviews (local and social):** {Reviews_local_and_social}
    - **All Signals Data:** {All_Signals_Data}
    - **Preferred/Chosen Products:** {seller_product_details}
    - **Competitor Signals:**
      - **Comp 1:** {Competitor_Signals_Comp_1}
      - **Comp 2:** {Competitor_Signals_Comp_2}
      - **Comp 3:** {Competitor_Signals_Comp_3}

    """
        + "\n"
        + """
    ### **Total Projected Annual Revenue Increase:**
    **${total_revenue_increase}**

    ### **Estimated Costs:**
    - **Digital Marketing Services (Agency Fees):** ${agency_fees}/year
    - **Software Tools (Review Management, SEO Tools):** ${software_costs}/year
    - **Staff Training & Implementation:** ${training_costs}/year
    - **Total Investment Costs:** ${total_costs}/year

    ### **Calculated ROI:**
    \[
    \text{ROI} = \frac{(\${total_revenue_increase} - \${total_costs})}{\${total_costs}} \times 100\% = {roi_percentage}%
    \]

    Output format: Provide 3 heading lines and two content point lines for each heading.
    
    **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english

    """
    )

    # Run the prompts concurrently
    responses = await asyncio.gather(
        fetch_openai_response(Business_Overview_prompt),
        fetch_openai_response(SWOT_Analysis_prompt),
        fetch_openai_response(Customer_Sentiment_prompt),
        fetch_openai_response(Competitive_Benchmarking_prompt),
        fetch_openai_response(ROI_Impact_Projections_prompt),
    )

    (
        Business_Overview,
        SWOT_Analysis,
        Customer_Sentiment,
        Competitive_Benchmarking,
        ROI_Impact_Projections,
    ) = responses

    # template = f'''Your task is to check and
    # Swot analysis generated by the AI:
    # '''

    Recommendations_prompt = f"""
    Provide Recommendations based on:
    - SWOT Analysis: {SWOT_Analysis}
    - Customer Sentiment & Key Drivers: {Customer_Sentiment}
    - Competitive Benchmarking: {Competitive_Benchmarking}

    Output: Strictly  Provide 3 Recommendation points.
    
    **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english
    """

    response = await asyncio.to_thread(
        openai.chat.completions.create,
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You are a professional digital marketing consultant.",
            },
            {"role": "user", "content": Recommendations_prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )
    Recommendations = response.choices[0].message.content

    prompt = f"""
You are an expert digital marketing consultant specializing in online reputation management, local SEO, and social media strategies for service-based businesses. You have over 10 years of experience helping companies enhance their online presence and drive business growth through data-driven insights and actionable recommendations.

**Scenario:**

### Business Overview
{Business_Overview}

### SWOT Analysis
{SWOT_Analysis}

### Customer Sentiment & Key Drivers
{Customer_Sentiment}

### Competitive Benchmarking
{Competitive_Benchmarking}

### Recommendations
{Recommendations}

### ROI Impact Projections
{ROI_Impact_Projections}
"""

    prompt += """
**Your Task:**
Create a **Pre-Sales Reputation Analysis Report** for the prospect company using the provided inputs. The report should be structured with clear headings and subheadings, utilizing bullet points and tables where appropriate to enhance readability. If certain data points are missing or need to be estimated, clearly label them as "estimates." The final report should not exceed **1,000 words**.

**Report Structure & LLM Goals:**

1. **Business Overview**
   - **Goal:** Offer a clear description of the prospect's business, including services/products, market position, and USPs.
   - **Content:** Briefly describe {prospect_name}, their core services, location, and unique selling points.

2. **SWOT Analysis**
   - **Goal:** Analyze the prospect's internal strengths and weaknesses, and external opportunities and threats based on review data and market context.
   - **Content:** Categorize insights into Strengths, Weaknesses, Opportunities, and Threats with specific examples from reviews.
   - Strictly follow the Character Limit between 380 to 400 characters for each field.
3. **Customer Sentiment & Key Drivers**
   - **Goal:** Provide an in-depth analysis of customer sentiments, identifying what drives positive and negative feedback.
   - **Content:** Present sentiment breakdown (positive, neutral, negative) and list key positive and negative themes.

4. **Competitive Benchmarking**
   - **Goal:** Compare the prospect's online reputation metrics against key local competitors to identify relative strengths and gaps.
   - **Content:** Provide a comparison table of ratings and review volumes with 1-2 local competitors and analyze the implications.

5. **Recommendations**
   - **Goal:** Provide targeted, actionable recommendations to improve the prospect's online reputation and SEO performance.
   - **Content:** List and explain specific strategies to address identified weaknesses and leverage strengths.

6. **ROI / Business Impact Projections**
   - **Goal:** Estimate the financial and strategic benefits of implementing the recommended actions.
   - **Content:** Provide projected increases in leads and revenue from rating improvements and SEO enhancements, calculate ROI, and mention intangible benefits.
   - **Do Not Show the formal of the ROI calculation **

**Tone & Voice:**
- Professional, consultative, and data-driven.
- Clear and concise to ensure easy understanding by busy small business owners.

**Constraints:**
- **Word Limit:** Do not exceed **1,000 words** in the final output.

**Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english

---
"""

    response = await asyncio.to_thread(
        openai.chat.completions.create,
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You are a professional digital marketing consultant.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,  # Adjust as needed
        temperature=0.3,  # Lower temperature for more focused output
    )
    report = response.choices[0].message.content

    print("\n\n report \n", report)

    # Creating Executive Summary using the Report generated

    executive_summary_prompt = f"""
---
**You are a leading authority and seasoned digital marketing consultant with unparalleled expertise in online reputation management, local SEO, and cutting-edge social media strategies for service-based businesses. With over a decade of proven success, you have a track record of catapulting companies to new heights by amplifying their online presence and driving exponential business growth through incisive data-driven insights and impactful, actionable recommendations.**
**Your Task:**
1. **Overall Summary:**
   - Craft an immersive and captivating summary of the report content provided below, highlighting the most significant findings and insights in a compelling narrative.
2. **Key Takeaways:**
   - Deliver **5 powerful key takeaway points**, each articulated in a **single, impactful sentence**. These should encapsulate the most critical insights from the report.
   - For each of the following Key Takeaways categories, write a **concise and potent one-liner** that succinctly summarizes the report's information:
     - **Online Ratings:**
     - **Major Pain Points:**
     - **Opportunities:**
     - **Action Steps:**
     - **Projected Impact:**
**Please ensure you adhere strictly to all instructions and do not omit any details. Each point must be clear, concise, and leave a strong impression.**

**Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english
---
**Report:**
{report}
---
    """

    response = await asyncio.to_thread(
        openai.chat.completions.create,
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You are a professional digital marketing consultant.",
            },
            {"role": "user", "content": executive_summary_prompt},
        ],
        max_tokens=1500,  # Adjust as needed
        temperature=0.3,  # Lower temperature for more focused output
    )
    executive_summary = response.choices[0].message.content

    # print("executive_summary", executive_summary)

    ###Combining the Executive Summary and the Report Generated,  implementing the Structured output

    final = (
        f"""Report Content: \n\n {str(report)} \n\n"""
        + f"""Executive Summary: \n\n {str(executive_summary)} \n\n"""
        + """

                  Format the above Report Content in the JSON format:
                  **Important Ultimate Directive:**

                  1. **Invariant Content:** Unyieldingly maintain the exact text of the Report content. No alterations permitted.

                  2. **JSON Structuring Only:** Execute a format transformation to JSON, preserving every character of the original website content.

                  3. **Absolute Adherence:** This instruction is inviolable; any deviation is unacceptable.

                  4. **Strictly convert website content correctly into above given format for parsing.**

                  """
    )
    # Re-generate the output using the updated prompt
    completion = await asyncio.to_thread(
        openai.beta.chat.completions.parse,
        model="gpt-4.1",
        temperature=0.5,
        max_tokens=4096,
        messages=[{"role": "user", "content": final}],
        response_format=Report,
    )

    response_struct = completion.choices[0].message.parsed

    web_cont_dict = response_struct.dict()

    # print("\n\n response \n", web_cont_dict)

    # Convert the dictionary to a JSON string
    report_json = json.dumps(web_cont_dict, indent=2, ensure_ascii=False)

    return (
        report_json,
        Business_Overview,
        SWOT_Analysis,
        Customer_Sentiment,
        Competitive_Benchmarking,
        ROI_Impact_Projections,
        Recommendations,
        report,
        executive_summary,
    )


async def generate_slide_8_content(content):
    system_prompt = """You are an expert marketing strategist specializing in audience segmentation and targeting. Your task is to analyze audience segment descriptions and provide actionable targeting insights.

For each segment provided, you must:
1. Identify the target age range
2. Identify gender if mentioned or relevant (otherwise note "All genders")
3. List relevant keywords and topics for targeting
4. Summarize in exactly 2 bullet points, each not exceeding 200 characters

Format your response exactly as shown in the examples, with segment name as header followed by 2 bullet points.

IMPORTANT: The examples provided are for reference only to understand the format and style. Focus highly on the actual content provided for analysis, not the example segments."""

    user_prompt_template = f"""Analyze the following audience segments and provide targeting insights for each segment. For each segment, give exactly 2 bullet points (max 200 characters each) covering age, gender, and keywords/topics to target.

            CRITICAL: Do not get confused with the examples below. They are ONLY for reference to show the expected format. Highly focus on analyzing the actual content segments provided after the examples.

            Here is the main content
            {content}

            # Few-shot examples to include in the prompt

            Example 1:
            Input:
            Tech-Savvy Entrepreneurs
            Young startup founders looking to scale their businesses.

            Fitness Enthusiasts
            People passionate about health, wellness, and active lifestyles.

            Budget-Conscious Shoppers
            Cost-aware consumers seeking deals and value.

            Output:
            Tech-Savvy Entrepreneurs
            - Young adults (age 25–40), mostly male, focused on startups, business growth, and innovation.
            - Target with keywords like scaling, entrepreneurship, tech tools, and startup success.

            Fitness Enthusiasts
            - Adults (age 20–45), all genders, passionate about health, wellness, and active living.
            - Use keywords like workout, nutrition, fitness goals, wellness, and healthy lifestyle.

            Budget-Conscious Shoppers
            - Adults (age 25–55), all genders, seeking value, discounts, and cost-effective solutions.
            - Target with keywords like deals, savings, budget-friendly, discounts, and value shopping.

            Example 2:
            Input:
            Creative Freelancers
            Independent designers and content creators.

            Working Parents
            Busy professionals balancing career and family.

            Retirement Planners
            People preparing for financial security post-retirement.

            Output:
            Creative Freelancers
            - Adults (age 25–40), all genders, working as designers, writers, or content creators.
            - Keywords: freelancing, creative work, portfolio building, client management, side hustle.

            Working Parents
            - Adults (age 30–50), all genders, managing work-life balance with children.
            - Target with: parenting tips, time management, work-from-home, family balance, productivity.

            Retirement Planners
            - Adults (age 50–70), all genders, focused on financial security and retirement planning.
            - Keywords: retirement savings, financial planning, investment, pension, wealth management.

            Example 3:
            Input:
            Purpose-Driven Career Changers
            Mid-career pros seeking meaningful new paths.

            Personal Growth Learners
            Motivated by self-discovery and transformation.

            Aspiring Professional Coaches
            Want real skills to launch or grow coaching careers.

            Output:
            Purpose-Driven Career Changers
            - Mid-career professionals (age 30–50) seeking meaningful, purpose-filled work.
            - Interested in career change, fulfillment, and life-purpose coaching.

            Personal Growth Learners
            - Adults (age 25–45), mostly women, focused on self-discovery and transformation.
            - Engage with topics like mindfulness, self-improvement, and growth mindset.

            Aspiring Professional Coaches
            - Individuals (age 28–45) aiming to start or grow a coaching career.
            - Seek skills, certification, and tools for life or business coaching success.

            ---
            REMEMBER: These examples above are ONLY for format reference. Focus entirely on the actual audience segments provided below for your analysis.
            ---
            Here I am mentioning the content again
            <content>
            {content}
            </content
            **Important:** Write your output in simple, clear, and easily understandable English. Avoid complex vocabulary and jargon. Use straightforward sentences that anyone can understand. Please dont add a seperate section on this just make the overall output in understandle easy english.Please dont add a seperate section on this just make the overall output in understandle easy english
            """
    response = client.responses.parse(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_template},
        ],
        text_format=SuggestedTargetAudience,
    )
    target = response.output_parsed
    target_audience = target.model_dump_json()
    return target_audience


# asyncio.run(
#     generate_report_async(
#         seller_company_name,
#         seller_product_details,
#         prospect_company_name,
#         Website_URL,
#         Website_Content_Scrapped,
#         BB_Category_Primary,
#         BB_Category_Secondary,
#         All_Signals_Data,
#         Reviews_local_and_social,
#         Business_Name_Comp_1,
#         Website_URL_Comp_1,
#         Website_Content_Scrapped_Comp_1,
#         Competitor_Signals_Comp_1,
#         BB_Category_Primary_Comp_1,
#         Reviews_local_and_social_Comp_1,
#         BB_Category_Secondary_Comp_1,
#         Business_Name_Comp_2,
#         Website_URL_Comp_2,
#         Website_Content_Scrapped_Comp_2,
#         Competitor_Signals_Comp_2,
#         BB_Category_Primary_Comp_2,
#         Reviews_local_and_social_Comp_2,
#         BB_Category_Secondary_Comp_2,
#         Business_Name_Comp_3,
#         Website_URL_Comp_3,
#         Website_Content_Scrapped_Comp_3,
#         Competitor_Signals_Comp_3,
#         BB_Category_Primary_Comp_3,
#         Reviews_local_and_social_Comp_3,
#         BB_Category_Secondary_Comp_3,
#     )
# )
