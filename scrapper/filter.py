import os
import ast
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Use GPT-3.5 and extract brand deal links
system_prompt = "You help extract brand deal or sponsored segment links"
user_prompt = """
The following is a YouTube description. Please extract the brand deal or sponsored segment links from the description.
Just return the links in an array only. Don't return anything else.
Here's the description
'''
{description}
'''
"""


def extract_brand_deal_links(description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt.format(description=description),
            },
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    urls_str = response.choices[0]["message"]["content"]
    # Convert to list
    urls = ast.literal_eval(urls_str)
    return urls


temp_description = """
This is a video about some of the many times we have nearly blown up the world. Part of this video is brought to you by Henson -- head over to
https://hensonshaving.com/veritasium and enter code 'Veritasium' for 100 free blades with the purchase of a razor. Make sure to add both the razor and the blades to your cart for the code to take effect. 

▀▀▀
References:
List of Broken Arrows -- https://ve42.co/AtomicArchive https://ve42.co/BrokenArrowsReport
Declassified Goldsboro Report -- https://ve42.co/Goldsboro
Operation ChromeDome -- https://ve42.co/OperationChromeDome
CIA website -- https://ve42.co/CIA

Cataclysmic cargo: The hunt for four missing nuclear bombs after a B-52 crash -- https://ve42.co/WoPo
THE LAST FLIGHT OF HOBO 28 -- https://ve42.co/lastflight
The Voice of Larry Messinger is from this documentary -- https://ve42.co/Messinger
Even Without Detonation, 4 Hydrogen Bombs From ’66 Scar Spanish Village -- https://ve42.co/NYTPalomares
Decades Later, Sickness Among Airmen After a Hydrogen Bomb Accident -- https://ve42.co/NYTPalomares2
Picture of ReVelle -- https://ve42.co/JackReVelle1
Great NPR where the audio of ReVelle is from -- https://ve42.co/JackReVelle2
CIA Website -- https://ve42.co/CIA


▀▀▀
Special thanks to our Patreon supporters:
Anton Ragin, Balkrishna Heroor, Bernard McGee, Bill Linder, Burt Humburg, Dave Kircher, Diffbot, Evgeny Skvortsov, Gnare, Jesse Brandsoy, John H. Austin, Jr., john kiehl, Josh Hibschman, Juan Benet, KeyWestr, Lee Redden, Marinus Kuivenhoven, Mario Bottion, MaxPal, Meekay, meg noah, Michael Krugman, Orlando Bassotto, Paul Peijzel, Richard Sundvall, Sam Lutfi, Stephen Wilcox, Tj Steyn, TTST, Ubiquity Ventures

▀▀▀
Directed by Petr Lebedev
Written by Petr Lebedev and Derek Muller
Edited by Peter Nelson
Animated by Fabio Albertelli, Jakub Misiek, Ivy Tello and Mike Radjabov
Filmed by Derek Muller 
Produced by Petr Lebedev and Derek Muller
Additional video/photos supplied by Getty Images and Pond5
Music from Epidemic Sound
"""
print(extract_brand_deal_links(temp_description))
