import requests
from bs4 import BeautifulSoup


def process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    
    name = ""
    hall_ticket_number = ""
    
    total_score = 0
    maths_score = 0
    physics_score = 0
    chemistry_score = 0

    sections = soup.find_all("div", class_="section-cntnr")
    if sections:
        for section in sections:
            section_lbl = section.find("div", class_="section-lbl")
            section_name = section_lbl.text.strip().lower() if section_lbl else ""
            
            section_score = 0
            for question in section.find_all("div", class_="question-pnl"):
                try:
                    correct_option = int(question.find("td", class_="rightAns").text[0])
                    chosen_option = int(question.find_all("td", class_="bold")[-1].text)
                    if correct_option == chosen_option:
                        section_score += 1
                except (ValueError, IndexError, AttributeError):
                    pass
            
            total_score += section_score
            if "mathematics" in section_name:
                maths_score = section_score
            elif "physics" in section_name:
                physics_score = section_score
            elif "chemistry" in section_name:
                chemistry_score = section_score
    else:
        for question in soup.find_all("div", class_="question-pnl"):
            try:
                correct_option = int(question.find("td", class_="rightAns").text[0])
                chosen_option = int(question.find_all("td", class_="bold")[-1].text)
                if correct_option == chosen_option:
                    total_score += 1
            except (ValueError, IndexError, AttributeError):
                pass
                
    target_name = soup.find("td", text="Hall Ticket Number")
    if target_name:
        hall_ticket_number = target_name.find_next_sibling().text
    target_hall_ticket = soup.find("td", text="Participant Name")
    if target_hall_ticket:
        name = target_hall_ticket.find_next_sibling().text
        
    return {
        "score": total_score,
        "name": name,
        "hall_ticket_number": hall_ticket_number,
        "maths_score": maths_score,
        "physics_score": physics_score,
        "chemistry_score": chemistry_score
    }
