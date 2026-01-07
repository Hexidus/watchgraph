"""
Seed EU AI Act compliance requirements into the database.
Based on EU AI Act Articles 9-15 (High-Risk AI System Requirements)
"""

from database import SessionLocal, init_db
from models import ComplianceRequirement, RiskCategory
import json

def seed_eu_ai_act_requirements():
    """Seed EU AI Act requirements into the database"""
    
    db = SessionLocal()
    
    # Check if requirements already exist
    existing = db.query(ComplianceRequirement).first()
    if existing:
        print("⚠️  Requirements already seeded. Skipping...")
        db.close()
        return
    
    requirements = [
        # Article 9: Risk Management System
        {
            "article": "Article 9",
            "title": "Risk Management System",
            "description": "High-risk AI systems shall be designed and developed with a risk management system that is iterative throughout the entire lifecycle, regularly reviewed and updated.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 9.2",
            "title": "Risk Management - Identification and Analysis",
            "description": "The risk management system shall identify and analyze known and foreseeable risks associated with each high-risk AI system.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 9.3",
            "title": "Risk Management - Mitigation Measures",
            "description": "Implement appropriate risk mitigation measures to address risks identified in the risk management process.",
            "applies_to": ["high"]
        },
        
        # Article 10: Data and Data Governance
        {
            "article": "Article 10.1",
            "title": "Training, Validation and Testing Data Quality",
            "description": "Training, validation and testing data sets shall be subject to appropriate data governance and management practices, including examination for possible biases.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 10.2",
            "title": "Data Relevance and Representativeness",
            "description": "Training, validation and testing data sets shall be relevant, representative, free of errors and complete.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 10.3",
            "title": "Data Set Properties Documentation",
            "description": "Data sets shall have appropriate statistical properties with regard to the intended purpose, including as regards the persons or groups on whom the system is intended to be used.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 10.5",
            "title": "Personal Data Processing",
            "description": "To the extent personal data is processed, measures shall be taken to ensure an appropriate level of quality in accordance with GDPR requirements.",
            "applies_to": ["high"]
        },
        
        # Article 11: Technical Documentation
        {
            "article": "Article 11.1",
            "title": "Technical Documentation Preparation",
            "description": "Technical documentation of the high-risk AI system shall be drawn up before the system is placed on the market or put into service and kept up-to-date.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 11.2",
            "title": "System Description and Specifications",
            "description": "Documentation shall include a general description of the AI system, its intended purpose, and detailed specifications of the system elements.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 11.3",
            "title": "Development Process Documentation",
            "description": "Document the design and development process, including information about the programming and training methodologies and techniques used.",
            "applies_to": ["high"]
        },
        
        # Article 12: Record-keeping
        {
            "article": "Article 12.1",
            "title": "Automatic Logging Capability",
            "description": "High-risk AI systems shall be designed with capabilities enabling automatic logging of events over the system's lifetime.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 12.2",
            "title": "Log Traceability and Analysis",
            "description": "Logging capabilities shall ensure a level of traceability appropriate to the intended purpose of the system, enabling post-market monitoring and investigation.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 12.3",
            "title": "Log Data Protection",
            "description": "Logging shall be designed to ensure the integrity and confidentiality of the logged information, with appropriate safeguards against tampering.",
            "applies_to": ["high"]
        },
        
        # Article 13: Transparency and Information Provision
        {
            "article": "Article 13.1",
            "title": "User Instructions and Information",
            "description": "High-risk AI systems shall be designed to operate with appropriate transparency, enabling users to interpret the system's output and use it appropriately.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 13.2",
            "title": "Instructions for Use",
            "description": "Provide clear and comprehensive instructions for use, including information about the system's capabilities and limitations.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 13.3",
            "title": "Transparency Obligations",
            "description": "Users shall be informed that they are interacting with an AI system, unless this is obvious from the circumstances.",
            "applies_to": ["high", "limited"]
        },
        
        # Article 14: Human Oversight
        {
            "article": "Article 14.1",
            "title": "Human Oversight Measures",
            "description": "High-risk AI systems shall be designed with appropriate human oversight measures, including human-in-the-loop, human-on-the-loop, or human-in-command approaches.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 14.2",
            "title": "Override Capability",
            "description": "The oversight measures shall ensure that users can intervene in the AI system's operation or interrupt it through a stop button or similar procedure.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 14.3",
            "title": "Human Understanding of System",
            "description": "Ensure that individuals assigned to human oversight have the necessary competence, training and authority to carry out their role.",
            "applies_to": ["high"]
        },
        
        # Article 15: Accuracy, Robustness and Cybersecurity
        {
            "article": "Article 15.1",
            "title": "Accuracy Requirements",
            "description": "High-risk AI systems shall achieve appropriate levels of accuracy, robustness and cybersecurity, and perform consistently throughout their lifecycle.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 15.2",
            "title": "Robustness Against Errors",
            "description": "Systems shall be resilient against errors, faults or inconsistencies that may occur within the system or the environment.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 15.3",
            "title": "Cybersecurity Measures",
            "description": "Technical and organizational measures shall be taken to ensure the cybersecurity of the AI system, including protection against unauthorized access.",
            "applies_to": ["high"]
        },
        {
            "article": "Article 15.4",
            "title": "Resilience to Attacks",
            "description": "Systems shall be resilient against attempts by unauthorized third parties to alter their use, outputs or performance.",
            "applies_to": ["high"]
        },
        
        # Limited Risk - Transparency Requirements
        {
            "article": "Article 52.1",
            "title": "AI System Disclosure",
            "description": "Users must be informed when they are interacting with an AI system, unless this is obvious from the context.",
            "applies_to": ["limited"]
        },
        {
            "article": "Article 52.3",
            "title": "Synthetic Content Labeling",
            "description": "AI-generated content (deepfakes, synthetic media) must be clearly labeled as artificially generated or manipulated.",
            "applies_to": ["limited"]
        },
    ]
    
    print(f"📝 Seeding {len(requirements)} EU AI Act requirements...")
    
    for req_data in requirements:
        requirement = ComplianceRequirement(
            article=req_data["article"],
            title=req_data["title"],
            description=req_data["description"],
            applies_to=json.dumps(req_data["applies_to"])  # Store as JSON string
        )
        db.add(requirement)
    
    db.commit()
    print(f"✅ Successfully seeded {len(requirements)} requirements!")
    db.close()

if __name__ == "__main__":
    # Initialize database tables first
    init_db()
    
    # Seed requirements
    seed_eu_ai_act_requirements()
    
    print("\n🎉 Database seeding complete!")
    print("Run your FastAPI server to see the requirements in action.")