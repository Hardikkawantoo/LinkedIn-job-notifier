import os
import concurrent.futures
from jobspy import scrape_jobs
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SENDER_EMAIL = #Add your email that sends the 
SENDER_PASSWORD = #Add your emails app password
RECEIVER_EMAIL = #Add your email that receives the 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
LOCATION = "Bengaluru, Karnataka, India"

SEARCH_TERMS = [
    "Java Developer",
    "backend developer", 
    "software developer", 
    "SDE 2", 
    "SDE 1", 
    "full stack developer"
]
# ==========================================

def scrape_single_term(term):
    """Worker function to scrape a single job title."""
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🔄 Scrape started: '{term}'")
    try:
        # Looking for jobs posted in the last hour
        jobs = scrape_jobs(
            site_name=["linkedin"],
            search_term=term,
            location=LOCATION,
            results_wanted=25, 
            country_api_name="india",
            hours_old=1
        )
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Scrape finished: '{term}' (Found {len(jobs)})")
        return jobs
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Error on '{term}': {e}")
        return pd.DataFrame()

def send_email_report(df):
    """Formats the data into an HTML table and sends the email."""
    print("📬 Preparing email report...")
    
    # Extract and rename columns
    report_df = df[['title', 'company', 'job_url']].copy()
    report_df.columns = ['Role Name', 'Company Name', 'Job Link']
    
    # Convert URLs to clickable HTML links
    report_df['Job Link'] = report_df['Job Link'].apply(
        lambda x: f'<a href="{x}">Apply Here</a>' if pd.notnull(x) else "N/A"
    )
    
    html_table = report_df.to_html(index=False, escape=False)
    
    html_body = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; font-size: 16px; }}
          table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
          th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
          th {{ background-color: #f2f2f2; }}
          tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
      </head>
      <body>
        <h2>Latest LinkedIn Job Openings</h2>
        <p>Found <b>{len(df)}</b> unique positions matching your criteria.</p>
        {html_table}
      </body>
    </html>
    """
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"LinkedIn Job Alert - {len(df)} New Roles"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("🎉 Email sent successfully!")
    except Exception as e:
        print(f"❌ Email delivery failed: {e}")

def job_scraping_cycle():
    """Executes the parallel scraping, data deduplication, and email dispatch."""
    all_jobs_list = []
    print(f"\n🚀 --- Starting Job Search Cycle at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    # Run up to 3 searches concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_term = {executor.submit(scrape_single_term, term): term for term in SEARCH_TERMS}
        for future in concurrent.futures.as_completed(future_to_term):
            jobs = future.result()
            if not jobs.empty:
                all_jobs_list.append(jobs)

    # Process results if any jobs were found
    if all_jobs_list:
        combined_jobs = pd.concat(all_jobs_list, ignore_index=True)
        
        # Deduplicate based on LinkedIn's unique job ID
        if 'id' in combined_jobs.columns:
            combined_jobs.drop_duplicates(subset=['id'], inplace=True)

        # Dispatch the email alert directly (No local saving)
        send_email_report(combined_jobs)
    else:
        print("No new jobs found during this run. Skipping email.")

if __name__ == "__main__":
    print("🤖 Scraper initialized. Running a single execution cycle without local saving.")
    
    # Execute the scrape exactly once
    job_scraping_cycle()
    
    print("\n🏁 Execution complete. Exiting script.")
