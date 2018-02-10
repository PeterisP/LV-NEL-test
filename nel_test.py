#!/usr/bin/python
# -*- coding: utf-8 -*-

# Full-text search of entity alternate names within the corpus.
# No disambiguation

from nel_baseline import load_entity_data, do_nel

if __name__ == "__main__":
    # execute only if run as a script

	entity_filename = 'wikidata/entities.json'
	trie, entities_by_name = load_entity_data(entity_filename)

	sample_text = "Emocionāla un vizuāli skaista Phjončhanas olimpisko spēļu atklāšanas ceremonija ir aiz muguras. Jau sestdien sākas sacensības, arī Latvijas sportistiem, bet šoreiz uzsvēršu dažas nianses, kas palika ārpus televīzijas translācijas.\n\nLaikam sākumā jāatvainojas lasītājiem, ka neizdevās \"Delfi\" teksta tiešraidē piedāvāt emocijas no stadiona. Par to, diemžēl, parūpējās pasākuma rīkotāji. Man bija ierādīta sēdvieta ar galdu, lai varētu informēt par notiekošo, bet šoreiz tam nebija nekādas nozīmes. Ja olimpiskā stadiona preses centrā bija pieejams internets, tad stadiona tribīnēs internets vairs nebija pieejams. Un tas radīja problēmas daudziem pasaules medijiem. Koreja sevi reklamē kā vienu no vadošajām valstīm tehnoloģiju attīstībā, bet šoreiz viņiem gadījās liels misēklis. Solījumi ātri atrisināt problēmu tā arī palika solījumu līmenī..\n\nBet ierašanās uz olimpisko stadionu bija patīkami raita. Ar brīvprātīgo palīdzību skatītāji, sponsoru pārstāvji, sporta federāciju viesi un mediju pārstāvji tika novirzīti pa attiecīgo eju un ātri varēja tikt iekšā svētku arēnā.\n\nMāte Daba šoreiz pielāgojās olimpiskajām spēlēm. Ja vēl dažas dienas pirms atklāšanas ceremonijas tika solīts samērā liels aukstums (pēc sajūtām), tad piektdienas vakarā nebija tik traki. Protams, bija ziemas apstākļi, jo tomēr ir ziemas olimpiskās spēles, bet nebija traki. Rīkotāji bija sagatavojušies, medijiem piedāvājot speciālu atklāšanas ceremonijas rokas somu, kurā bija ne tikai siltie krēslu paliktnīši, bet arī speciālie kāju/ roku sildāmie.\n\nRīkotāji bija labi parūpējušies par valstu izcelšanu, jo ar gaismas starmešu palīdzību valsts nosaukums un karogs vizuāli parādījās tribīnēs. Patiešām iespaidīgi klātienē un īpaši sirdi kustinoši, kad iesoļoja Latvijas delegācija. Jo reti tik lielos sporta pasākumos Latvija ir redzama ar tik lielu uzrakstu un tik lielu sarkanbaltsarkano karogu.\n\nAtšķirībā no citām atklāšanas ceremonijām, šoreiz bija padomāts par sportistiem, kuriem nebija ilgi jāgaida uz savu iznākšanu. Domāju, ka sportisti to novērtēja.\n\nPirms atklāšanas ceremonijas un atklāšanas ceremonijas laikā sociālajos tīklos popularitāti iemantoja divu pasaules valstu līderi – Donalds Tramps un Kims Čenuns. Tie gan nebija īstie ASV un Ziemeļkorejas līderi, lai gan par Trampa iespējamo ierašanos tika runāts. Lai gan tie bija viltus Tramps un Čenuns, uz brīdi šie abi kungi ar parastajām skatītāju biļetēm iemantoja mediju un pārējo uzmanību. Televīzijas translācijā, protams, to neatļāvās rādīt.\n\nNākamais uzmanības vērtais fakts ir Krievijas sportistu izsoļošana un ar Krievijas sportistiem saistītie skandāli. Krievijas olimpisko atlētu (OAR) sagaidīšana bija divējāda – tribīnēs bija gan aplausi, gan svilpieni un ūjināšana. Olimpisko karogu pirms OAR delegācijas nesa brīvprātīgais, jo diez vai Krievijā saprastu kāda sportista uzņemšanos nest ne savu karogu. Krievijas žurnālisti tribīnēs, ieraugot parādes sākumā izgaismotos valstu lielos uzrakstus un karogus tribīnēs, ar nožēlu konstatēja – ekh, mums neredzēt Krievijas karogu...\n\nKrievijas dopinga skandāla tēma pastarpināti bija manāma gan SOK prezidenta Tomasa Baha uzrunā, gan sportistu, treneru un tiesnešu kopējā zvērestā. Runas ne tikai par dopinga izskaušanu un cīņu pret to, bet arī par godīgu cīņu. Godīga cīņa visos aspektos.\n\nDelegāciju parādē bija vēl viens jaunievedums no organizatoru puses. Delegāciju \"lēnāko\" pārstāvju stūmēji. Citreiz olimpiskajās spēlēs valstu parādi kavē atraktīvākie sportisti, kuri mēdz ilgāk soļot pa stadionu. Šoreiz \"bīstamākajām\" delegācijām kā pēdējie gāja brīvprātīgie, kuri neļāva atpalikt no savas komandas.\n\nValstis atklāšanas ceremonijās cenšas izcelties ar apģērbiem, lai izpelnītos \"atzīmes\" par stilu. Šoreiz augstāko atzīmi saņēma ne jau lielās delegācijas, bet gan mazās valstis. Līdzīgi kā pirms pusotra gada Rio vasaras olimpiskajās spēlēs, izcēlās Tongas pārstāvis Pita Taufatofua, kurš Phjončhanas olimpiskajā stadionā izsoļoja puspliks. Un tas notika brīdī, kad pēc sajūtām stadionā bija ap -10 grādiem pēc Celsija.\n\nĀrpus ētera palika neliels incidents pēc valstu iznākšanas. Nākamā muzikālā izpildījuma laikā kāds vīrs pamanījās noslīdēt pa uztaisīto sniega nogāzi un tad vēl fonā centās dziedāt. Protams, ātri apsardzes darbinieki kungu satvēra un izvadīja no stadiona.\n\nNeesmu tik detalizēti sekojis līdzi iepriekšējām olimpisko spēļu atklāšanas ceremonijām, bet, iespējams, vienu no pirmajām reizēm SOK prezidents bija kopā ar sportistiem. Un vēl iespaidīgāk šoreiz izskatījās tas, ka Bahs runu teica, fonā esot apvienotās Korejas sportistiem. Apvienotās Korejas iznākšana vētrainas ovācijas izraisīja vēl pirms parādīšanās stadionā, jo komanda bija redzama izejā uz tuneli. Iznākšana bija īpaši emocionāla, stadionā līdzjutēji sportistus sveica stāvot kājās, bet, kā vēlāk norādīja acīgie televīzijas skatītāji, Ziemeļkorejas diktatora Kima Čenuna jaunākā māsa Kima Jočena stadionā šajā brīdī sēdēja.\n\nAtklāšanas ceremonija ir aiz muguras. To noslēdza krāšņs, ugunīgs šovs, bet jau sestdien sāksies īstā cīņa – 16 dienu garumā 92 valstu sportisti sadalīs 102 medaļu komplektus. Cerams, ka Latvija nepaliks \"sausā\" un arī Korejā skanēs Latvijas himna."
	mentions = do_nel(trie, entities_by_name, sample_text)
	print(mentions)

	print('Done')