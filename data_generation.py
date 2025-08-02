import random
import uuid
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

transcript_templates = [
    [
        "Salesperson: Hello, is this {customer_name}?",
        "Recipient: Yes, this is {customer_name}.",
        "Salesperson: Hi {customer_name}, I'm {agent_name} from {company}. I'd like to talk about our {product}.",
        "Recipient: Hmm, I'm not sure if we need that.",
        "Salesperson: Actually, {product} can help you save costs and improve efficiency. It's perfect for businesses like yours.",
        "Recipient: Sounds interesting, but we're on a tight budget.",
        "Salesperson: I understand. We're offering a limited-time discount. Would you like to try a free demo?",
        "Recipient: Maybe later. We're just not ready now.",
        "Salesperson: No worries, {customer_name}. Thanks for your time!"
    ],
    [
        "Salesperson: Hi, is this {customer_name}?",
        "Recipient: Yes, who's this?",
        "Salesperson: I'm {agent_name} from {company}. I'm calling to introduce our new {product}.",
        "Recipient: Oh, what's special about it?",
        "Salesperson: It's eco-friendly and cost-efficient. Great for daily use.",
        "Recipient: That sounds useful. What's the price?",
        "Salesperson: It normally sells at ${price}, but we have a {discount}% discount.",
        "Recipient: Cool. I'll take one.",
        "Salesperson: Awesome! Your order is being processed. Thank you, {customer_name}!"
    ],
    [
  "Salesperson: Hi, is this {customer_name}?",
  "Recipient: Yes, who's this?",
  "Salesperson: I'm {agent_name} from {company}. I'm calling to introduce our new Apple AirPods Pro (2nd Generation).",
  "Recipient: Oh, what's special about it?",
  "Salesperson: They're eco-friendly and packed with tech—active noise cancellation, immersive sound, and sleek design. Great for daily use.",
  "Recipient: That sounds useful. What's the price?",
  "Salesperson: It normally sells at $249, but we have a 10% discount and free shipping, plus extra discounts for students, military, and seniors.",
  "Recipient: Cool. I’ll think about it. Do you offer any warranty?",
  "Salesperson: Absolutely. It comes with a 1-year warranty and our full support.",
  "Recipient: That sounds fair. I’d love to read some reviews though.",
  "Salesperson: I’ll email you verified customer reviews. Would you also like to hear about future promotions?",
  "Recipient: Yes please.",
  "Salesperson: Awesome! Your order is being processed. Thank you, {customer_name}!"
   ],
   [
  "Salesperson: Hi, is this {customer_name}?",
  "Recipient: Yes, who's this?",
  "Salesperson: I'm {agent_name} from {company}. I'm reaching out about the certified refurbished Apple AirPods Pro, perfect for work-from-home productivity.",
  "Recipient: Oh, what makes them special?",
  "Salesperson: They feature Active Noise Cancellation, immersive 3D audio, and come with a 1-year warranty. Great for focus and comfort.",
  "Recipient: That’s interesting. What's the price?",
  "Salesperson: They're $239 with up to $50 in savings, plus a 10% student discount if eligible.",
  "Recipient: I am a student. Can you verify my ID?",
  "Salesperson: Yes, just confirm your student ID or enrollment status over the phone.",
  "Recipient: Great. Can I also get accessories and do a trade-in?",
  "Salesperson: Absolutely! We can bundle in accessories and offer trade-in credit based on your old device.",
  "Recipient: Sounds perfect.",
  "Salesperson: Awesome! Your order is being processed. Thank you, {customer_name}!"
  ],
  [
  "Salesperson: Hi, is this {customer_name}?",
  "Recipient: Yes, who's this?",
  "Salesperson: I'm {agent_name} from {company}. I'm calling to introduce the new Dell Inspiron 15 5000 laptop.",
  "Recipient: Oh, what's special about it?",
  "Salesperson: It's sleek, powerful, and perfect for work or play. With up to 12 hours of battery and Intel i7 processors.",
  "Recipient: That sounds useful. What's the price?",
  "Salesperson: Base model is $599, mid-range at $799, and high-end at $999. Right now, we’re offering a free $99 hard drive and accessory bundles.",
  "Recipient: Do you offer discounts too?",
  "Salesperson: Yes! 10% off for students, 5% for military, and free accessories worth $50.",
  "Recipient: Nice. What about warranty and support?",
  "Salesperson: All laptops come with Dell’s 1-year warranty and premium support options.",
  "Salesperson: Awesome! Your order is being processed. Thank you, {customer_name}!"
   ],
   [
  "Salesperson: Hi, is this {customer_name}?",
  "Recipient: Yes, who's this?",
  "Salesperson: I'm {agent_name} from {company}. I'm calling about the new iPhone 14 Pro Max.",
  "Recipient: Oh, what's special about it?",
  "Salesperson: It has an A16 chip, 120Hz display, and a quad-camera for stunning photos and videos. Perfect for multitaskers and content creators.",
  "Recipient: That sounds powerful. What's the price?",
  "Salesperson: Models start at around $999, but with our 10% discount and free AppleCare+, plus bonus gifts like AirPods or storage upgrades, it’s a steal.",
  "Recipient: Sounds tempting. What about warranty and support after a year?",
  "Salesperson: AppleCare+ extends your warranty up to 3 years, and we also offer referral credits worth $200.",
  "Recipient: Great. I’m leaning toward the 256GB model.",
  "Salesperson: Awesome! Your order is being processed. Thank you, {customer_name}!"
  ]   
]

companies = ["GreenTech Inc.", "Brita", "EcoHome", "HydroPure", "SmartClean", "Dell", "LG", "Samsung", "HP"]
products = ["EcoCycle", "SmartWater Bottle", "HydroBooster", "AirFilter Pro", "RecycleMate", "Laptop", "TV", "Tab"]

def generate_transcript():
    template = random.choice(transcript_templates)
    agent_name = fake.name()
    customer_name = fake.last_name()
    company = random.choice(companies)
    product = random.choice(products)
    price = random.randint(30, 70)
    discount = random.choice([5, 10, 15])


    transcript = "\n".join([
        line.format(
            agent_name=agent_name,
            customer_name=customer_name,
            company=company,
            product=product,
            price=price,
            discount=discount
        )
        for line in template
    ])
    return transcript

def generate_call():
    call_id = str(uuid.uuid4())
    agent_id = str(uuid.uuid4())[:8]
    customer_id = str(uuid.uuid4())[:8]
    language = "en"
    start_time = fake.date_time_between(start_date="-60d", end_date="now").isoformat()
    transcript = generate_transcript()
    words = len(transcript.split())
    duration_seconds = int((words / 120.0) * 60)  # avg 120 wpm → seconds

    return {
        "call_id": call_id,
        "agent_id": agent_id,
        "customer_id": customer_id,
        "language": language,
        "start_time": start_time,
        "duration_seconds": duration_seconds,
        "transcript": transcript
    }

def generate_dataset(n=250, filename="call_transcripts1.json"):
    calls = [generate_call() for _ in range(n)]
    with open(filename, "w") as f:
        json.dump(calls, f, indent=2)
    print(f"Generated {n} transcripts and saved to {filename}")


generate_dataset()



