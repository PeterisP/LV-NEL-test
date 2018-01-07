# Adapted from https://github.com/LUMII-AILab/FrameMerger/blob/master/src/DocumentUpload.py
import re

def fixName(name):
    fixname = re.sub('[«»“”„‟‹›〝〞〟＂]', '"', name, re.UNICODE)  # Aizvietojam pēdiņas
    fixname = re.sub("[‘’‚`‛]", "'", fixname, re.UNICODE)
    return fixname

def personAliases(name):
    insertalias = [name] 
    if re.match(r'[A-ZĀČĒĢĪĶĻŅŠŪŽ]\w+ [A-ZČĒĢĪĶĻŅŠŪŽ]\w+$', name, re.UNICODE):
        extra_alias = re.sub(r'([A-ZČĒĢĪĶĻŅŠŪŽ])\w+ ', r'\1. ', name, flags=re.UNICODE )
        if not extra_alias in insertalias:
            insertalias.append(extra_alias)
        extra_alias = re.sub(r'([A-ZČĒĢĪĶĻŅŠŪŽ])\w+ ', r'\1.', name, flags=re.UNICODE )
        if not extra_alias in insertalias:
            insertalias.append(extra_alias)
    return insertalias

orgTypes = [
    ['SIA', 'Sabiedrība ar ierobežotu atbildību'],
    ['AS', 'A/S', 'Akciju sabiedrība'],
    ['apdrošināšanas AS', 'Apdrošināšanas akciju sabiedrība'],
    ['ZS', 'Z/S', 'Zemnieka saimniecība'],
    ['IU', 'Individuālais uzņēmums'],
    ['Zvejnieka saimniecība'],
    ['UAB'],
    ['VAS'],
    ['valsts aģentūra'],
    ['biedrība'],
    ['fonds'],
    ['mednieku biedrība'],
    ['mednieku klubs'],
    ['mednieku kolektīvs'],
    ['kooperatīvā sabiedrība'],
    ['nodibinājums'],
    ['komandītsabiedrība'],
    ['zvērinātu advokātu birojs'],
    ['advokātu birojs'],
    ['partija'],
    ['dzīvokļu īpašnieku kooperatīvā sabiedrība'],
    ['dzīvokļu īpašnieku biedrība'],
    ['Pilnsabiedrība', 'PS']
    ]

def orgAliases(name):
    aliases = set()
    aliases.add(name)
    representative = name

    fixname = fixName(name)
    aliases.add(fixname)
    if re.match(r'^"[^"]+"$', fixname, re.UNICODE):
        fixname = fixname[1:-1] # noņemam pirmo/pēdējo simbolu, kas ir pēdiņa
        aliases.add(fixname)

    if re.search(r'vidusskola', fixname, re.UNICODE): # vidusskolu saīsinājumi
        aliases.add(re.sub('vidusskola', 'vsk.', fixname, re.UNICODE))
        aliases.add(re.sub('vidusskola', 'vsk', fixname, re.UNICODE))

    understood = False
    for orgGroup in orgTypes:
        maintitle = orgGroup[0]
        clearname = None
        #TODO - šos regexpus varētu 1x sagatavot un nokompilēt, ja paliek par lēnu
        p1 = re.compile(r'^"([\w\s\.,\-\'\+/!:\(\)@&]+)" ?, (%s)$' % '|'.join(orgGroup), re.UNICODE) # "Kautkas", SIA
        m = p1.match(fixname)
        if m:
            clearname = m.group(1)
        p2 = re.compile(r'^(%s) " ?([\w\s\.,\-\'\+/!:\(\)@&]+) ?"$' % '|'.join(orgGroup), re.UNICODE) # SIA "Kautkas"
        m = p2.match(fixname)
        if m:
            clearname = m.group(2)

        if clearname:
            understood = True            
            representative = '%s "%s"' % (maintitle, clearname)  # SIA "Nosaukums"
            aliases.add(representative)
            for title in orgGroup:  # Visiem uzņēmējdarbības veida variantiem
                aliases.add('%s "%s"'     % (title, clearname)) # SIA "Nosaukums"
                aliases.add('%s %s'       % (title, clearname)) # SIA Nosaukums
                aliases.add('%s, %s'      % (clearname, title)) # Nosaukums, SIA
                aliases.add('"%s", %s'    % (clearname, title)) # "Nosaukums", SIA
                aliases.add('"%s"'        % (clearname, ))      # "Nosaukums"
                # aliases.add('%s'          % (clearname, ))      # Nosaukums   TODO - šis ir bīstams!   A/S "Dzintars" pārvērtīsies par Dzintars, kas konfliktēs ar personvārdiem, līdzīgi ļoti daudz firmu kam ir vietvārdi, utml
                # modifikācijas ar atstarpēm, kādas liek morfotageris
                aliases.add('" %s " , %s' % (clearname, title)) # " Nosaukums " , SIA  
                aliases.add('%s " %s "'   % (title, clearname)) # SIA " Nosaukums "
                aliases.add('" %s "'      % (clearname, ))      # " Nosaukums "
            break # nemeklējam tālāk

    if not understood:
        if not '"' in fixname and re.search(r' (partija|pārvalde|dome|iecirknis|aģentūra|augstskola|koledža|vēstniecība|asociācija|apvienība|savienība|centrs|skola|federācija|fonds|institūts|biedrība|teātris|pašvaldība|arodbiedrība|[Šš]ķīrējtiesa)$', fixname, re.UNICODE):
            aliases.add( clearOrgName(fixname) )
            understood = True # 'hardkodētie' nosaukumi kuriem bez standartformas citu aliasu nebūs
        elif re.search(r'(filiāle Latvijā|Latvijas filiāle|korporācija|biedrība|krājaizdevu sabiedrība|klubs|kopiena|atbalsta centrs|asociācija)$', fixname, re.UNICODE):
            aliases.add( clearOrgName(fixname) )
            understood = True # šādus nevar normāli normalizēt

    if not understood:
        # print 'Not understood', fixname # debuginfo - ja ir "labs" avots kur itkā vajadzētu būt 100% sakarīgiem nosaukumiem
        aliases.add( clearOrgName(fixname) )

    aliases.remove(representative)
    return [representative] + list(aliases)


 # mēģina attīrīt organizāciju nosaukumus no viskautkā
def clearOrgName(name): 
    norm = re.sub('[«»“”„‟‹›〝〞〟＂"‘’‚‛\']', '', name, re.UNICODE)  # izmetam pēdiņas
    norm = re.sub('(AS|SIA|A/S|VSIA|VAS|Z/S|Akciju sabiedrība) ', '', norm, re.UNICODE)  # izmetam prefiksus
    norm = re.sub(', (AS|SIA|A/S|VSIA|VAS|Z/S|Akciju sabiedrība)', '', norm, re.UNICODE)  # ... postfixotie nosaukumi ar komatu
    norm = re.sub(' (AS|SIA|A/S|VSIA|VAS|Z/S|Akciju sabiedrība)', '', norm, re.UNICODE)  # ... arī beigās šādi reizēm esot bijuši
    norm = re.sub('\s\s+', ' ', norm, re.UNICODE)  # ja nu palika dubultatstarpes
    return norm
