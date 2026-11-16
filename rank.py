"""Rank Summer 2027 software engineering internships against a resume profile.

Usage:
    python3 rank.py path/to/listings.json ranked.json

listings.json comes from the public SimplifyJobs list:
    https://github.com/SimplifyJobs/Summer2027-Internships  (.github/scripts/listings.json)
"""
import json, sys, time, re

LA = ['los angeles','santa monica','irvine','pasadena','el segundo','culver city','burbank','torrance','long beach','glendale','playa vista','costa mesa','newport beach','hawthorne','redondo beach','manhattan beach','carson','anaheim','westlake','thousand oaks','calabasas','woodland hills','van nuys','marina del rey','venice','santa ana','tustin','fullerton','huntington beach','lake forest','aliso viejo','sherman oaks','inglewood','downey','palmdale','simi valley','camarillo','pomona','riverside','mission viejo','laguna','seal beach','gardena','cerritos','brea','cypress','agoura','northridge','chatsworth','valencia','santa clarita','lancaster','ontario','universal city','studio city','north hollywood','hollywood','west hollywood','beverly hills','century city','el monte','alhambra','monrovia','san pedro','wilmington','orange']
NON_US = ['canada','toronto','vancouver','montreal','waterloo','ottawa','london, uk','united kingdom','india','bangalore','bengaluru','hyderabad','singapore','germany','ireland','mexico','japan','china','hong kong','australia','israel','poland','netherlands','france','spain','brazil']
DEFENSE = ['anduril','lockheed','northrop','raytheon','rtx','boeing','general dynamics','l3harris','booz allen','leidos','saic','aerospace corporation','aerovironment','palantir','shield ai','bae systems','mitre','caci','spacex','blue origin','sierra nevada','textron','huntington ingalls','saronic','epirus','castelion','hadrian','varda','impulse space','voyager','rocket lab']


def is_la(locs):
    for l in locs:
        ll = l.lower().strip()
        if ll in ('la', 'los angeles', 'los angeles, ca', 'los angeles, california'):
            return True
        city, _, st = ll.partition(',')
        st = st.strip()
        if city.strip() in LA and st in ('ca', 'la', 'california', ''):
            return True
    return False


def score(x):
    t = x['title'].lower()
    locs = ' | '.join(x.get('locations') or []).lower()
    degrees = x.get('degrees') or []
    why, flags, s = [], [], 0

    # Hard filters: grad-level roles, non-bachelor's roles, non-US roles
    if re.search(r'\bph\.?d\b|\bmaster|\bmba\b|\bgraduate\b|\bsenior\b|\bsr\.?\b|\bstaff\b|new grad|grad student', t):
        return None
    if degrees and "Bachelor's" not in degrees and "Associate's" not in degrees:
        return None
    us = [l for l in (x.get('locations') or []) if not any(n in l.lower() for n in NON_US)]
    if not us:
        return None

    # Location
    if is_la(x.get('locations') or []):
        s += 30; why.append('LA / Orange County')
    elif ', ca' in locs or 'california' in locs:
        s += 12; why.append('California')
    if 'remote' in locs:
        s += 8; why.append('Remote option')

    # Role fit
    if re.search(r'software (engineer|engineering|developer|development)|\bswe\b|developer|programmer', t):
        s += 15; why.append('Core software role')
    if re.search(r'c\+\+|\bjava\b|embedded|firmware|systems|backend|back-end|game|gameplay|tools', t):
        s += 8; why.append('Uses your C++/Java/systems skills')
    if re.search(r'sophomore|freshman|early|explore|discover|first[- ]year|launch|pathways|diversity|veteran', t):
        s += 10; why.append('Early-career / pipeline program')
    if re.search(r'machine learning|\bml\b|\bai\b|data science|quant|research', t):
        s -= 6; flags.append('Leans ML/research: your resume shows less here')
    if re.search(r'front|web|ui\b|ios|android|mobile|full[- ]?stack', t):
        s -= 2; flags.append('Web/mobile stack not on your resume yet')
    if any(k in x['company_name'].lower() for k in DEFENSE):
        s += 6; why.append('Defense/aerospace: veteran background is a plus')
        flags.append('Often requires U.S. citizenship / clearance eligibility')

    # Freshness
    age = (time.time() - x['date_posted']) / 86400
    if age <= 7:
        s += 10; why.append('Posted this week')
    elif age <= 30:
        s += 5; why.append('Posted this month')
    elif age > 120:
        s -= 5; flags.append('Posted 4+ months ago: may be filling up')

    return {
        'id': x['id'], 'company': x['company_name'], 'title': x['title'], 'locations': us,
        'url': x['url'], 'posted': time.strftime('%Y-%m-%d', time.gmtime(x['date_posted'])),
        'score': s, 'tier': 'Strong' if s >= 45 else ('Good' if s >= 25 else 'Possible'),
        'why': why, 'flags': flags,
    }


def main():
    d = json.load(open(sys.argv[1]))
    out = []
    for x in d:
        if not (x.get('active') and x.get('is_visible')):
            continue
        if 'Summer 2027' not in (x.get('terms') or []):
            continue
        if x.get('category') not in ('Software', 'Software Engineering'):
            continue
        r = score(x)
        if r:
            out.append(r)
    out.sort(key=lambda r: -r['score'])
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
    print(len(out))


if __name__ == '__main__':
    main()
