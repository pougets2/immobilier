from multiprocessing.pool import Pool
from bs4 import BeautifulSoup

import grequests
import pandas as pd
import requests
import asyncio
import re
import time
import sys
import random
from datetime import date



# Numéros de pages à parser
PAGE_INIT = 0
PAGE_LAST = 100

# Affichage de la progression
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# Definition du corps d'une annonce
class PageBundle:
    prix = []
    adresses = []
    les_urls = []
    nombre_de_chambre = []
    nombre_de_SDB = []
    nombre_de_sejour = []
    surfaces = []
    description = []
    Neuf_ou_ancien = []
    Auction = []
    Aide = []

# Autres variables globales
start_time = time.time()
counter = 0
p = PageBundle()
requete_non_aboutie = 0
# Parsing du contenu d'une page
def parse_page(page):
    global counter, p, requete_non_aboutie

    # Update de la barre de progression
    counter += 1
    print_progress(counter-1, 100*70)

    # Parsing de la page
    connected = False

    while not connected:
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            connected = True
            annonces = soup.find_all(class_="listing-results-wrapper")
            if annonces != []:
                p.prix += [re.sub("[^0-9]", "", annonce.find(class_="listing-results-price text-price").get_text())
                           if re.sub("[^0-9]", "", annonce.find(class_="listing-results-price text-price").get_text()) != ''
                           else "NA" for annonce in annonces]
                p.adresses += [annonce.find(class_="listing-results-address").get_text() for annonce in annonces]
                p.les_urls += ["https://www.zoopla.co.uk/" + annonce.find(class_="status-wrapper").find("a")['href'] for
                               annonce in
                               annonces]
                p.nombre_de_chambre += [
                    annonce.find('span', {"class": "num-icon num-beds"}).get_text() if annonce.find('span', {
                        "class": "num-icon num-beds"}) is not None else "NA" for annonce in annonces]
                p.nombre_de_SDB += [
                    annonce.find('span', {"class": "num-icon num-baths"}).get_text() if annonce.find('span', {
                        "class": "num-icon num-baths"}) is not None else "NA" for annonce in annonces]
                p.nombre_de_sejour += [
                    annonce.find('span', {"class": "num-icon num-reception"}).get_text() if annonce.find('span', {
                        "class": "num-icon num-reception"}) is not None else "NA" for annonce in annonces]
                p.surfaces += [str(int(
                    re.sub("[^0-9]", "", annonce.find('span', {"class": "num-icon num-sqft"}).get_text())) * 0.092903) if
                               (annonce.find('span', {"class": "num-icon num-sqft"}) is not None) and
                               ("ft" in annonce.find('span', {"class": "num-icon num-sqft"}).get_text()) else
                               str((re.sub("[^0-9]", "",
                                           annonce.find('span', {"class": "num-icon num-sqft"}).get_text())) if
                                   annonce.find('span', {"class": "num-icon num-sqft"}) is not None else "NA") for annonce
                               in annonces]
                p.description += [annonce.find('h2', class_="listing-results-attr").get_text().splitlines()[1] for annonce
                                  in annonces]
                p.Neuf_ou_ancien += ["N" if annonce.find(class_="status-text status-text-new-home") is not None else "A" for
                                     annonce in
                                     annonces]
                p.Auction += ["Enchères" if "auction" in str(annonce.find('p')).lower() else "vente" for annonce in
                              annonces]
                p.Aide += ["Help to buy" if "help to buy" in str(annonce.find('p')).lower() else "NA" for annonce in
                           annonces]

        except AttributeError:
            requete_non_aboutie += 1
            connected = True

# Charger toutes les pages d'une manière asynchrone
def load_pages():
    global PAGE_INIT
    outil = ['OX49', 'B61', 'M23', 'OL4', 'LU1', 'AB55', 'B24', 'PA64', 'WN8', 'DG8', 'PL5', 'TN36', 'PO38', 'BD15',
             'RH77', 'HS5', 'GU23', 'KW12', 'KT9', 'PA37', 'BN52', 'CO14', 'IP22', 'DT10', 'EH43', 'NN6', 'W1G', 'B26',
             'CT1', 'UB8', 'TR26', 'DG4', 'TS18', 'PA29', 'CR5', 'BD24', 'SN9', 'NE82', 'CW6', 'KA9', 'KA10', 'EH38',
             'PO9', 'BH21', 'BH7', 'RM3', 'RM10', 'NE43', 'KA30', 'YO32', 'PL29', 'TW5', 'SG10', 'CT4', 'OX29', 'NE1',
             'WR13', 'N13', 'WF8', 'NE27', 'CA13', 'NE41', 'BS22', 'TQ4', 'PE27', 'TR3', 'DE3', 'LA22', 'EH5', 'HU3',
             'DA15', 'DE23', 'PL32', 'KA27', 'L36', 'BN8', 'G32', 'SY19', 'DH3', 'KY14', 'HS4', 'CH88', 'SP7', 'SA43',
             'GU24', 'DN15', 'AB37', 'BN88', 'EH19', 'UB7', 'PH23', 'NG1', 'M22', 'CB6', 'DY4', 'CF3', 'BT17', 'B70',
             'TS1', 'LU2', 'EX19', 'S25', 'YO25', 'LA17', 'EX12', 'N2', 'AB30', 'OL11', 'TN32', 'SO40', 'KT12', 'BS21',
             'LS7', 'CW10', 'MK12', 'WC2B', 'SA41', 'MK8', 'CA26', 'IG1', 'EH6', 'TA16', 'FK18', 'LL33', 'IP13', 'CH8',
             'AB14', 'LL44', 'NP24', 'M5', 'M18', 'B6', 'SS99', 'CF82', 'G82', 'BN51', 'EC4P', 'PA4', 'LE41', 'BT26',
             'KW3', 'PA68', 'ST3', 'IP31', 'DY5', 'CV37', 'MK4', 'IP18', 'WC2N', 'TQ12', 'DL12', 'IV45', 'CM0', 'HP7',
             'NN4', 'WC2E', 'BD99', 'SL9', 'KA8', 'LE94', 'OL5', 'TA1', 'G4', 'ST8', 'GU31', 'SG12', 'SS22', 'TN39',
             'EX21', 'HG2', 'CF37', 'GU4', 'L69', 'BS40', 'SA99', 'HP8', 'NE47', 'GU33', 'KT14', 'LE3', 'RM2', 'PR11', 'SS4', 'HS3', 'DG12', 'W1C', 'PO35', 'PR3', 'PA36', 'LD7', 'SG4', 'PA63', 'PE25', 'ML2', 'PH25', 'IG11', 'HU9', 'GU7', 'DN1', 'SY5', 'TS3', 'BS27', 'PA31', 'B20', 'NG8', 'HR6', 'CM4', 'TN26', 'YO42', 'GL50', 'BH12', 'BA14', 'WF12', 'TS9', 'SW95', 'LA12', 'EH27', 'TF8', 'HS6', 'GU6', 'N16', 'IP21', 'TD7', 'SN3', 'KT7', 'S65', 'TW9', 'SN15', 'EC4R', 'WS15', 'PR6', 'ML5', 'ML7', 'EH8', 'WF7', 'LA18', 'NE25', 'RG1', 'SA32', 'B67', 'OX13', 'WV99', 'GU17', 'LL38', 'PH41', 'CF23', 'BB12', 'PL28', 'SW1E', 'EC1P', 'IG6', 'EH3', 'TA6', 'SA48', 'SY13', 'BN7', 'PE26', 'CM17', 'CM9', 'WC1E', 'EH40', 'LU5', 'LL37', 'FY7', 'B35', 'EH54', 'AL8', 'MK19', 'PA12', 'PE8', 'JE1', 'TA15', 'NR99', 'M31', 'BL6', 'BH25', 'IV63', 'N6', 'IV21', 'SA20', 'HU20', 'TS27', 'BR4', 'IM99', 'NR9', 'SE26', 'N11', 'N8', 'XM4', 'B2', 'M25', 'HP14', 'GU9', 'GU30', 'BT5', 'EC3V', 'AL4', 'WV15', 'PA75', 'DE1', 'NG19', 'IV5', 'B13', 'PE19', 'BN14', 'DT8', 'DA11', 'HD8', 'DT7', 'L12', 'BL0', 'SY10', 'TF11', 'KW10', 'CF33', 'B15', 'CO2', 'BS16', 'KY15', 'NG90', 'YO14', 'CO8', 'ZE2', 'WC1A', 'CV36', 'CM77', 'B71', 'DN21', 'FK11', 'PA3', 'BN3', 'CF63', 'TR21', 'PH44', 'FY4', 'M14', 'FK13', 'NW10', 'RG12', 'PO18', 'W8', 'EC2Y', 'GL53', 'DY14', 'CH64', 'NP25', 'ZE1', 'SP4', 'OX15', 'IP20', 'CF99', 'E17', 'GU25', 'NE30', 'GU18', 'BT94', 'SY24', 'KW7', 'IP9', 'SA14', 'N14', 'PA62', 'IP7', 'TN4', 'OX3', 'LD4', 'N20', 'L39', 'NE49', 'SA10', 'CR6', 'DH6', 'TA3', 'ME17', 'EC3M', 'PA43', 'LL30', 'CB7', 'BT48', 'M19', 'TF12', 'CA22', 'CH65', 'LL56', 'AB23', 'WN3', 'AL3', 'E15', 'DA12', 'CO16', 'NR14', 'G14', 'HX7', 'KW2', 'NE18', 'E12', 'EX36', 'DN9', 'DL6', 'L20', 'GU22', 'B62', 'ML12', 'KY8', 'PE22', 'LN11', 'NG5', 'TR19', 'NW11', 'L24', 'SK23', 'NG33', 'BT36', 'TR25', 'SW2', 'NW2', 'SY3', 'TW6', 'SL60', 'CB21', 'NR25', 'DN36', 'SA36', 'WA16', 'BT60', 'LN7', 'KT5', 'G11', 'AB53', 'L14', 'IV36', 'PR5', 'SP11', 'DN8', 'DA3', 'CT6', 'M61', 'IV28', 'EH14', 'CM13', 'EH13', 'NG12', 'ST15', 'NW3', 'ML11', 'G46', 'BT14', 'WV10', 'IV55', 'TR2', 'NN12', 'PH30', 'CV5', 'LD1', 'HX5', 'PH15', 'S44', 'IP17', 'WR8', 'G33', 'SA31', 'LL62', 'PL6', 'WV12', 'PL25', 'JE2', 'BT68', 'IV42', 'RG22', 'LL60', 'SS7', 'NR29', 'CV47', 'RH5', 'S64', 'BT53', 'EC4N', 'BN23', 'B99', 'SG9', 'TS23', 'MK11', 'CB8', 'TR10', 'WD23', 'TF1', 'YO17', 'GU26', 'S99', 'CV13', 'IV52', 'DL3', 'S14', 'NE8', 'TQ10', 'BN50', 'IP3', 'SM3', 'HP20', 'BA11', 'B18', 'CM12', 'YO24', 'ME9', 'B46', 'OL10', 'ZE3', 'LS24', 'LS13', 'IV7', 'W2', 'ST19', 'IP26', 'M6', 'SW16', 'IP19', 'TA14', 'SA1', 'WA55', 'BH13', 'L2', 'M33', 'LL18', 'OX16', 'BL2', 'HP17', 'PO31', 'M24', 'CH28', 'BH31', 'SO30', 'EC1V', 'SR2', 'SE13', 'LL63', 'IV31', 'DE24', 'IV8', 'KA11', 'W1S', 'DE75', 'PE9', 'LL54', 'SW9', 'BN99', 'HU4', 'M26', 'BT45', 'LL32', 'CA15', 'TN28', 'HU8', 'CO1', 'BD98', 'B40', 'ME2', 'BA16', 'ML1', 'OX26', 'DN32', 'WR1', 'IV56', 'BT3', 'BN2', 'G40', 'RM14', 'DL15', 'SE12', 'KA20', 'EN8', 'EC3R', 'NE37', 'IP30', 'BT33', 'BT38', 'LS98', 'SE2', 'HS1', 'CW8', 'SO14', 'PA45', 'EX16', 'B65', 'IP16', 'EX24', 'ST10', 'CF11', 'CV23', 'SA64', 'KT21', 'GU20', 'S45', 'M44', 'G62', 'BB94', 'SY11', 'DD1', 'S81', 'PE4', 'NE10', 'CA27', 'NN13', 'BT81', 'CA28', 'G75', 'EX32', 'IV24', 'DH9', 'YO21', 'E5', 'NE4', 'S62', 'BH6', 'EX13', 'FK12', 'GU11', 'WC2A', 'DE65', 'WV6', 'PA9', 'GU12', 'LE2', 'B91', 'SA69', 'PH31', 'G45', 'HP13', 'CF64', 'PA16', 'BL11', 'SE4', 'CA19', 'ST4', 'CW11', 'BH10', 'SL7', 'LE7', 'TW10', 'PA21', 'DN12', 'NG18', 'NP20', 'LS4', 'BS11', 'YO12', 'TA7', 'LL67', 'DY2', 'EH25', 'DG7', 'S95', 'OL13', 'WR10', 'KA6', 'LA23', 'TQ14', 'BD17', 'S60', 'IV18', 'N7', 'WS2', 'SO50', 'CF47', 'PA60', 'PL15', 'SS1', 'TW19', 'IV16', 'TR1', 'KT22', 'DY6', 'SA66', 'HU17', 'WV8', 'IP25', 'OX20', 'NR4', 'SN10', 'PA20', 'WR15', 'SS14', 'LE16', 'BH4', 'GU32', 'BD2', 'WD7', 'PO3', 'EC4V', 'E3', 'TN21', 'PA66', 'B28', 'IG3', 'TN1', 'PL95', 'HP16', 'EH18', 'TR20', 'EC3A', 'CT12', 'BB8', 'LS2', 'HR3', 'SP9', 'KW15', 'FY3', 'SA40', 'RM12', 'L3', 'GL10', 'LL11', 'OX10', 'CF40', 'IM8', 'GL15', 'AB41', 'DH99', 'SA62', 'TN16', 'UB9', 'SE22', 'SA68', 'PL24', 'BS10', 'S10', 'PO33', 'CB4', 'CH26', 'ME8', 'SO21', 'NR15', 'FK7', 'LD3', 'SS8', 'SA38', 'SW19', 'HA1', 'DL98', 'DN19', 'CT20', 'HD6', 'BN9', 'RH11', 'M35', 'PO16', 'HP3', 'BB6', 'B27', 'CF24', 'PH9', 'L17', 'BB10', 'SK22', 'WF4', 'PA67', 'HG3', 'SA63', 'CT17', 'KA24', 'PL7', 'SA39', 'TR12', 'NN7', 'CB3', 'NR33', 'SY14', 'GU16', 'NE20', 'SY16', 'SA33', 'LU4', 'DE4', 'TW13', 'G81', 'TS16', 'PH12', 'KT10', 'EH11', 'M15', 'BT76', 'CH49', 'NW9', 'TA17', 'N17', 'NE28', 'SG14', 'N3', 'FK17', 'SA17', 'LL27', 'CT3', 'GU8', 'PH35', 'SR8', 'PO41', 'BT23', 'CF35', 'TR15', 'PA25', 'IV20', 'PH24', 'NP26', 'BA12', 'B37', 'CW7', 'SA2', 'ME10', 'LN4', 'WS13', 'LA16', 'PE5', 'WS8', 'B90', 'BN24', 'TD1', 'N5', 'EN3', 'PL30', 'CW9', 'M2', 'BD13', 'S80', 'CA24', 'BT9', 'W1H', 'TN20', 'CR2', 'CH3', 'TR14', 'TN23', 'RH2', 'GL14', 'NE70', 'BD7', 'CH61', 'PH49', 'CR4', 'PH34', 'S96', 'LL64', 'TS28', 'LE5', 'DN5', 'HR4', 'SA6', 'PA77', 'CF30', 'PO36', 'DE7', 'SM2', 'SO43', 'ME18', 'L22', 'AB54', 'AB13', 'LS5', 'LL21', 'HU10', 'NE67', 'DE11', 'KT23', 'PH4', 'BA5', 'PE6', 'EX9', 'WA6', 'W9', 'RM15', 'G72', 'TN18', 'WF3', 'PE35', 'ST20', 'BS48', 'WV4', 'GY10', 'G31', 'TN12', 'RH19', 'HU7', 'WC1X', 'HP19', 'KT3', 'NN14', 'UB5', 'JE4', 'WS11', 'G83', 'DE22', 'TF13', 'OL3', 'SS17', 'TA21', 'BH5', 'B72', 'SE25', 'RG6', 'PA69', 'KY16', 'WA7', 'CM2', 'PO6', 'NN1', 'GL1', 'WN7', 'KA28', 'B68', 'LL23', 'PO13', 'ME5', 'GU1', 'SM6', 'MK17', 'IV19', 'LS25', 'BT1', 'LA9', 'LL47', 'SA11', 'PA24', 'NG21', 'B14', 'NR18', 'RM4', 'M45', 'G44', 'CB23', 'M20', 'NN18', 'PE32', 'SN1', 'HP27', 'CV31', 'SN26', 'PL12', 'L9', 'DN3', 'EC3N', 'WF14', 'CA21', 'PL16', 'HU2', 'WV14', 'TQ1', 'PE36', 'EX20', 'PA8', 'DD6', 'W14', 'HS8', 'ML9', 'G64', 'WA8', 'BT61', 'BA6', 'WA2', 'NN29', 'RM1', 'RH7', 'CH48', 'HU16', 'BB2', 'KY4', 'NW26', 'DN2', 'TF2', 'LS14', 'NE88', 'HP6', 'KW9', 'PL2', 'EN4', 'B74', 'DA6', 'NP23', 'AL7', 'B60', 'LE67', 'S32', 'DD9', 'PH6', 'FK15', 'CB22', 'SA46', 'BT82', 'DL9', 'RG20', 'BL9', 'TN7', 'DN20', 'EH33', 'LL12', 'BT20', 'GY7', 'S2', 'SA34', 'PA65', 'HP5', 'NR11', 'CA20', 'TN25', 'SK4', 'NE36', 'RG10', 'BA1', 'OL95', 'TF6', 'NE11', 'BT74', 'WF9', 'NE65', 'B98', 'WN2', 'DH2', 'RG5', 'RG17', 'NG23', 'NW1W', 'RG30', 'BT10', 'WF5', 'SS12', 'TS21', 'ST2', 'DT6', 'DT3', 'CF15', 'SS9', 'SM7', 'CA12', 'PE1', 'OX4', 'B44', 'BL3', 'DA4', 'LE9', 'NE3', 'BT56', 'CM92', 'PL9', 'SY18', 'N19', 'CR9', 'TS13', 'B8', 'PA18', 'RG14', 'BN21', 'CM22', 'L4', 'EH46', 'LS15', 'HA8', 'SW6', 'KA17', 'TA4', 'WN1', 'IV15', 'G1', 'CH5', 'CA99', 'LN2', 'SA61', 'NN16', 'KW6', 'DA1', 'S3', 'TS8', 'PL11', 'KW11', 'IP98', 'RH9', 'PH40', 'L72', 'N1C', 'EC4M', 'EC2R', 'WC1R', 'HG5', 'SK6', 'SE27', 'PA22', 'LL29', 'WR6', 'G74', 'MK16', 'DG5', 'PE3', 'LS19', 'TN35', 'BS24', 'LE18', 'IG8', 'EX18', 'SR3', 'E98', 'PL23', 'PO30', 'S98', 'NN3', 'LE21', 'DE99', 'CM3', 'BT67', 'BN20', 'TD15', 'RG29', 'M16', 'BS49', 'KY11', 'CT14', 'NN15', 'EC2M', 'LS8', 'LE95', 'M28', 'OX33', 'LS88', 'WA4', 'IV46', 'DN16', 'NE61', 'WD24', 'GL20', 'EH16', 'SW10', 'G73', 'LD5', 'BS3', 'OX17', 'HP22', 'CF83', 'N1', 'TR9', 'S18', 'L11', 'HP4', 'NR5', 'SK2', 'MK5', 'EH2', 'EX14', 'SN12', 'CH4', 'LD8', 'S74', 'IV3', 'CF43', 'OX27', 'RH14', 'S41', 'KW8', 'KT1', 'RH18', 'PA76', 'SA16', 'CT19', 'PR4', 'WN4', 'MK13', 'B97', 'SE15', 'DL2', 'EH28', 'GU52', 'TR16', 'GY2', 'EH95', 'EH1', 'HS7', 'NG6', 'IP27', 'TA22', 'ST5', 'L33', 'AB43', 'BD14', 'WV5', 'W1D', 'CB2', 'PL3', 'LL65', 'AB25', 'PH32', 'NP7', 'DN6', 'BB4', 'BA21', 'LL16', 'SW20', 'SY9', 'PH42', 'SA19', 'L32', 'BN16', 'TN29', 'SK16', 'SN2', 'LS12', 'SR7', 'N18', 'CF81', 'BH19', 'TN2', 'LU7', 'AB11', 'SO42', 'LE11', 'BB9', 'M17', 'IP29', 'LS18', 'BN18', 'RM19', 'BN1', 'PR1', 'HA0', 'SM1', 'IM6', 'WV98', 'SY1', 'SA44', 'IP23', 'CH34', 'WD4', 'BT2', 'N15', 'AB21', 'BS41', 'CH62', 'IV32', 'SO52', 'SN6', 'NE31', 'EH55', 'E4', 'CF45', 'HD5', 'EN9', 'BD6', 'GU47', 'BT15', 'DE13', 'M99', 'B33', 'RM11', 'GIR', 'PH18', 'BH9', 'HD2', 'BT19', 'TW1', 'EH49', 'CA7', 'MK46', 'CW4', 'LN6', 'LL25', 'SO41', 'SO17', 'KA25', 'BN12', 'SN4', 'LL71', 'HU15', 'B96', 'RH17', 'MK43', 'WD3', 'HU1', 'BT7', 'SW14', 'NG17', 'G23', 'SS6', 'BS25', 'TS4', 'W3', 'BT16', 'NE35', 'CA1', 'TW3', 'NR28', 'IG7', 'M46', 'IV1', 'BT41', 'CA23', 'BL4', 'SA9', 'WV1', 'DE15', 'JE3', 'B78', 'LE12', 'ST11', 'WS9', 'SN8', 'SK5', 'NN8', 'DA7', 'CH60', 'GY6', 'DT9', 'IV4', 'B49', 'FK16', 'G70', 'WV13', 'TR8', 'TD6', 'UB18', 'L7', 'KY5', 'CA11', 'PR9', 'GU15', 'B64', 'DL5', 'TW7', 'SO31', 'HS2', 'SS15', 'EH45', 'PO4', 'HP1', 'SG18', 'CV1', 'S7', 'NG13', 'CF32', 'CA10', 'HD1', 'WR11', 'M43', 'KA15', 'B12', 'CH27', 'PH37', 'NN2', 'IM7', 'WS12', 'G61', 'YO18', 'BT78', 'CF71', 'W11', 'NP4', 'PL22', 'ME15', 'NR8', 'PE2', 'SE5', 'PO11', 'SY12', 'MK77', 'TA23', 'SS16', 'B25', 'NE48', 'HR8', 'PO17', 'G69', 'CA16', 'CM18', 'SY6', 'BT46', 'SK17', 'AB31', 'LL22', 'S36', 'G41', 'OX5', 'ML10', 'CA18', 'BS5', 'TA20', 'PE23', 'KW5', 'CA9', 'KW1', 'WA12', 'LL24', 'NE23', 'SW11', 'RG19', 'NR23', 'NG7', 'LL48', 'DE14', 'BH17', 'DN10', 'BS34', 'DE73', 'NR26', 'PR8', 'TR5', 'LN3', 'B23', 'PA73', 'WF13', 'LU6', 'ME99', 'NE99', 'PR7', 'HA4', 'TR4', 'GU29', 'WA9', 'SA12', 'SR43', 'LE87', 'NP15', 'HA2', 'CT8', 'WC1N', 'TS15', 'SO16', 'LS21', 'IV22', 'SY8', 'IV43', 'DY13', 'SK11', 'TA24', 'L16', 'BH23', 'LA7', 'BT63', 'SG6', 'TR18', 'GL19', 'CT16', 'TQ2', 'BT75', 'SK9', 'SW15', 'RM5', 'PL31', 'NW6', 'SL95', 'B29', 'CO12', 'SG19', 'RM8', 'S11', 'DN40', 'BN13', 'S42', 'NP10', 'SY23', 'M4', 'BS98', 'DE45', 'CB5', 'ML3', 'LL68', 'HD9', 'NP8', 'CA5', 'GL4', 'RM17', 'EX33', 'W1B', 'CA25', 'BD16', 'BT27', 'CM1', 'BT13', 'MK14', 'M7', 'BT64', 'BN22', 'RH10', 'LL73', 'TW16', 'NW1', 'TQ3', 'LL36', 'LA19', 'HU19', 'BT51', 'GU19', 'NE64', 'EH37', 'TS12', 'NR6', 'CF36', 'BD12', 'LS20', 'CT9', 'PA70', 'EX11', 'MK42', 'IP15', 'BT22', 'DN17', 'B11', 'HP21', 'LA10', 'B38', 'PO2', 'NG16', 'GY8', 'ML4', 'WR99', 'NE71', 'DN41', 'B63', 'GL56', 'G43', 'L40', 'BS14', 'GY3', 'SL4', 'PA6', 'DL7', 'WS1', 'IV99', 'CH30', 'ME1', 'BN26', 'SO23', 'PA7', 'MK44', 'NE40', 'MK1', 'KA21', 'GU10', 'DT11', 'BA13', 'LA8', 'BT42', 'BT80', 'BN95', 'IM5', 'WF15', 'HU11', 'B32', 'IP2', 'PL10', 'HX6', 'PL17', 'CH44', 'EH91', 'LS23', 'B77', 'SE21', 'CW98', 'TN24', 'SE17', 'CB1', 'B93', 'L38', 'ST9', 'BD9', 'PL13', 'DA14', 'S5', 'BH1', 'L80', 'YO8', 'DT4', 'IP28', 'GL3', 'SY99', 'BA10', 'IG4', 'SG17', 'IV23', 'DG6', 'BH22', 'BB3', 'GL2', 'TS5', 'PO37', 'CO4', 'YO60', 'NE42', 'PE30', 'KY12', 'KT4', 'EH12', 'EX39', 'GL7', 'SE6', 'G13', 'SA42', 'BT29', 'DD11', 'AB36', 'CB11', 'BT24', 'W10', 'NE22', 'YO31', 'SK13', 'PL21', 'CM23', 'LL14', 'SK10', 'TN9', 'NG11', 'WA14', 'PA47', 'NE13', 'E20', 'GU95', 'BN10', 'W1F', 'ST14', 'NE92', 'B10', 'SE1', 'GY9', 'EH24', 'SY17', 'BT92', 'SE16', 'ME7', 'N9', 'EX34', 'FK20', 'LA13', 'SP1', 'BS28', 'CF38', 'WN6', 'LL19', 'NG14', 'SE19', 'B94', 'PA11', 'L28', 'EH7', 'DN37', 'CM19', 'CM16', 'LE17', 'SY2', 'L18', 'TD10', 'IV40', 'LL58', 'NR2', 'DG2', 'DD2', 'LA5', 'PH19', 'M21', 'PH8', 'TA5', 'DY1', 'BL78', 'PH14', 'OX44', 'BR7', 'PA72', 'SA70', 'NR31', 'PA61', 'PA42', 'IP10', 'HD4', 'PE15', 'SK1', 'IV41', 'NP19', 'PA27', 'SW3', 'KT20', 'DN55', 'NG4', 'B4', 'EX7', 'WR12', 'NR12', 'B19', 'LE65', 'TN27', 'L6', 'BD1', 'G65', 'KA3', 'S63', 'PH17', 'PA17', 'TN13', 'DG16', 'HP23', 'EH23', 'CA3', 'S21', 'OX12', 'RG23', 'CF61', 'LA11', 'UB2', 'GL6', 'S73', 'SO32', 'B79', 'AB12', 'YO43', 'BT93', 'LL70', 'DD10', 'AB32', 'PO22', 'KA7', 'SW1X', 'SA80', 'IP12', 'SW17', 'HR2', 'WA10', 'TF5', 'TS20', 'EH44', 'EH4', 'EH39', 'FK9', 'GL17', 'LL76', 'SA13', 'W1J', 'RH8', 'AB56', 'DN18', 'BH20', 'SK12', 'SE23', 'SS11', 'PR25', 'TS7', 'YO90', 'BS30', 'W6', 'HA3', 'PL1', 'TD3', 'WV16', 'CH66', 'M1', 'RH20', 'LA15', 'SG13', 'BR5', 'NG24', 'M12', 'RM13', 'DN35', 'YO23', 'PA71', 'M8', 'G15', 'SL6', 'S71', 'CF44', 'EX31', 'WD17', 'PA49', 'OL6', 'KA18', 'DY8', 'BL5', 'LL77', 'CO13', 'DE55', 'MK2', 'SN11', 'LL40', 'TR23', 'LA14', 'SA71', 'EH9', 'BT37', 'WD25', 'HR5', 'NP13', 'CH41', 'W1T', 'RM18', 'YO30', 'PO10', 'CR8', 'CT5', 'CO9', 'S66', 'DG14', 'G9', 'KT17', 'BR8', 'BT44', 'YO22', 'GL13', 'NP12', 'EH10', 'LE15', 'CB25', 'MK10', 'CH63', 'AL9', 'RG40', 'PA35', 'EX4', 'RH4', 'OL8', 'TN33', 'BS37', 'KY13', 'KT11', 'B42', 'CF48', 'SO19', 'B30', 'CV9', 'BD20', 'SR6', 'SG7', 'SN38', 'FK2', 'E6', 'PL35', 'NE83', 'NG32', 'S9', 'BT49', 'NR13', 'DH1', 'WA13', 'NN10', 'PA28', 'CH2', 'CO15', 'AB52', 'CM15', 'HX2', 'IP1', 'DA2', 'TA13', 'OX1', 'CH43', 'PA34', 'YO26', 'SP3', 'TS14', 'NE2', 'BB18', 'LA6', 'DA9', 'UB10', 'TA2', 'ST17', 'AB39', 'SL5', 'SK7', 'DG13', 'PR26', 'RG41', 'BS26', 'MK7', 'WR2', 'SO22', 'PE11', 'SO45', 'PA44', 'ST16', 'KW17', 'KA4', 'KY9', 'CT7', 'PA48', 'RM16', 'E1', 'B69', 'BA2', 'SE14', 'MK6', 'YO19', 'BS39', 'PA30', 'LL75', 'HA5', 'EX3', 'LS99', 'BT43', 'NN11', 'EH17', 'BS1', 'EH26', 'PL26', 'GY1', 'S8', 'YO13', 'GU34', 'SP8', 'W1A', 'WR5', 'WC2H', 'NG34', 'CA17', 'PA80', 'W1K', 'DN39', 'E13', 'IP5', 'CV22', 'KY2', 'RG4', 'GL55', 'CH99', 'EC1N', 'WR4', 'L35', 'CF41', 'L15', 'CM5', 'S12', 'RG7', 'AB22', 'L23', 'CR90', 'SO24', 'PO20', 'CF5', 'RM7', 'CM7', 'BA7', 'S97', 'L67', 'N10', 'SA45', 'AB38', 'N81', 'LS9', 'W12', 'EH36', 'WN5', 'CV7', 'SA67', 'BT70', 'MK18', 'LS29', 'HR9', 'CH31', 'LE1', 'NR3', 'G21', 'SL2', 'OL7', 'CW2', 'AB10', 'SW1Y', 'NR16', 'TW20', 'BT35', 'KA5', 'G20', 'EN5', 'RG8', 'L8', 'CF91', 'BR2', 'IV51', 'GL9', 'LS11', 'CA8', 'NR21', 'TS19', 'RG31', 'SA5', 'RH15', 'SL1', 'MK45', 'LS28', 'L70', 'CM20', 'EH51', 'BS8', 'TR7', 'NG25', 'CW1', 'BH2', 'S26', 'UB1', 'FK6', 'FK3', 'EC2P', 'LL34', 'ST1', 'RH1', 'EH32', 'WA1', 'TW18', 'IV49', 'CB24', 'IV48', 'CF14', 'SA15', 'SA65', 'PH13', 'BA3', 'PA74', 'G71', 'NE12', 'G77', 'E18', 'SN16', 'CV11', 'BD18', 'TQ9', 'SR1', 'OX2', 'CH45', 'SW8', 'EX6', 'AB34', 'DG10', 'SG2', 'BS6', 'PE13', 'NE32', 'BN5', 'WV9', 'CH1', 'CA95', 'SS3', 'LS22', 'EN10', 'CH32', 'SK8', 'M34', 'AB24', 'LS17', 'YO7', 'L25', 'PE10', 'CA2', 'B66', 'UB4', 'CV34', 'BT77', 'B17', 'LL35', 'UB6', 'E16', 'HX3', 'GL54', 'CH42', 'G67', 'BB5', 'EX15', 'HX1', 'CM99', 'RG28', 'SG5', 'BT62', 'GL11', 'TN34', 'FK14', 'HP18', 'E14', 'SN25', 'LE13', 'FK5', 'CM24', 'RM9', 'N22', 'TR13', 'DL17', 'M29', 'BN42', 'SY22', 'LL46', 'HP11', 'GL5', 'LA20', 'HD3', 'BT34', 'IP11', 'WD99', 'G5', 'WD6', 'SW5', 'IG5', 'KT8', 'LL31', 'WA88', 'W1W', 'RG27', 'BS35', 'ME12', 'DA18', 'TN15', 'G3', 'TS11', 'NE69', 'SK15', 'LL28', 'G66', 'TN5', 'CH25', 'BB7', 'DN14', 'SO53', 'L10', 'BH3', 'WC1V', 'DE21', 'PA26', 'WF17', 'TD8', 'LE8', 'L19', 'M11', 'ST21', 'SO51', 'PA78', 'B48', 'SE24', 'G79', 'YO51', 'BT66', 'DN34', 'SS5', 'S70', 'M32', 'TN40', 'KT6', 'LN12', 'ST18', 'DA10', 'PH26', 'NG15', 'DG11', 'NR19', 'DL11', 'HP12', 'EH53', 'CR44', 'IM4', 'DD4', 'NR32', 'AB16', 'SR5', 'GU2', 'NN17', 'CV8', 'TW17', 'TS2', 'PO1', 'CF10', 'WC2R', 'SO15', 'DE6', 'DH98', 'IV13', 'AB44', 'NG10', 'RG24', 'SA4', 'EC4A', 'NR35', 'SE20', 'SA73', 'NW5', 'TF7', 'LL42', 'SS2', 'SK3', 'NE66', 'OX9', 'IV17', 'DH7', 'L26', 'LL39', 'WR7', 'HU6', 'RG42', 'IP8', 'PO34', 'TQ5', 'BN45', 'DE74', 'PE29', 'BS9', 'IV12', 'AB99', 'PA5', 'NG9', 'HR1', 'OL15', 'BS20', 'CV33', 'NR30', 'NE7', 'TA11', 'KA29', 'PL20', 'CF62', 'BH15', 'G84', 'NW7', 'NP16', 'EH48', 'PO14', 'LS1', 'DD8', 'NE19', 'ME19', 'OL14', 'LL52', 'LL59', 'YO41', 'M60', 'PH2', 'TA9', 'RG18', 'CF39', 'EX23', 'CT11', 'LL55', 'PL8', 'ML6', 'M38', 'NR1', 'NR7', 'PE14', 'LL41', 'CO5', 'PA19', 'CO11', 'TQ7', 'TN17', 'B73', 'TF10', 'BN17', 'CT13', 'G51', 'CT15', 'WV7', 'S4', 'W4', 'SS0', 'TQ6', 'S20', 'EH20', 'BT39', 'DN11', 'BS23', 'RG25', 'LS3', 'G76', 'BA9', 'L29', 'S6', 'KA2', 'GU51', 'B16', 'BS4', 'SM4', 'HG1', 'KT2', 'FK4', 'GU35', 'BA8', 'SW1V', 'YO1', 'LL17', 'CH47', 'PH43', 'N1P', 'DA17', 'BD10', 'DE5', 'TF3', 'BD19', 'IV26', 'GU28', 'SE8', 'IV6', 'PH16', 'BD22', 'RG45', 'PE16', 'G34', 'BS29', 'TN14', 'SY20', 'HU18', 'DL13', 'SY25', 'OX39', 'IM2', 'BD3', 'RH13', 'YO16', 'BS36', 'TW11', 'TS26', 'DN7', 'LE6', 'SW12', 'L31', 'S1', 'GL18', 'G90', 'CF72', 'CW3', 'CO6', 'PA32', 'TW4', 'IG9', 'WD19', 'B75', 'PE7', 'WR9', 'LL74', 'OX25', 'L1', 'CO3', 'CF46', 'BN6', 'BD23', 'BT55', 'OL12', 'S75', 'NE34', 'PH5', 'YO62', 'CF95', 'L68', 'SE11', 'KY10', 'DN22', 'WS3', 'CV35', 'WC1B', 'TD9', 'AB42', 'AB15', 'SN7', 'PA2', 'SA72', 'HS9', 'TD4', 'EX37', 'B1', 'WF2', 'PH20', 'EH35', 'KY3', 'LL69', 'BA20', 'LL53', 'DA5', 'CV21', 'ME11', 'WF90', 'NE26', 'B31', 'PH1', 'SA35', 'DN31', 'NE85', 'BT6', 'BA15', 'PH11', 'WS7', 'HG4', 'NG2', 'WR14', 'FY8', 'TD14', 'RG9', 'BN41', 'NE5', 'WS5', 'NE98', 'DA16', 'LE14', 'SE28', 'PL27', 'CH46', 'BT52', 'BT25', 'GU21', 'E8', 'SN99', 'HP9', 'TN19', 'KT15', 'KT19', 'DD5', 'B36', 'PA1', 'PH38', 'SO20', 'BS2', 'CA14', 'OX18', 'BH16', 'IP14', 'G52', 'PR2', 'SG11', 'ST13', 'EX8', 'EH52', 'CA6', 'IG2', 'SY4', 'SP5', 'NE46', 'BN11', 'KT16', 'GL8', 'EC1R', 'SG3', 'TN31', 'SP2', 'CW12', 'SA7', 'BD5', 'BD11', 'GU3', 'SN14', 'TD12', 'PA13', 'EN1', 'EC2A', 'EH42', 'KA19', 'NE68', 'M3', 'B80', 'N21', 'L27', 'EX17', 'CV2', 'SP10', 'BN43', 'LD2', 'CO7', 'BT28', 'SR4', 'MK9', 'SW1A', 'LL45', 'PE12', 'PL34', 'TN3', 'PE37', 'S43', 'AB33', 'IP32', 'BH11', 'LA3', 'DL8', 'EC1A', 'L74', 'PO32', 'LS10', 'TN11', 'BL8', 'SE10', 'TW12', 'TN6', 'SW1P', 'WV11', 'SS13', 'SN5', 'IP24', 'DH5', 'DE12', 'CT10', 'KY7', 'HA9', 'ME14', 'BS13', 'B47', 'ME4', 'CB10', 'DH8', 'NR34', 'HU13', 'GY5', 'DN33', 'BN15', 'CH7', 'LL57', 'BT12', 'AL6', 'TS10', 'OX28', 'EH34', 'CO10', 'UB11', 'NE9', 'IP4', 'W1U', 'PO8', 'PO40', 'NP18', 'NG20', 'B76', 'DN4', 'EC2V', 'BR6', 'ME13', 'EN7', 'DG1', 'CV10', 'EH99', 'SE18', 'PL4', 'MK15', 'TA19', 'EN2', 'BL1', 'NE39', 'HP15', 'S40', 'DT5', 'CA4', 'EH15', 'G42', 'SY21', 'RH16', 'LS6', 'PL14', 'PH7', 'PE24', 'EN77', 'CH29', 'SA18', 'PE28', 'PE20', 'WC1H', 'WF1', 'EH31', 'MK41', 'MK3', 'AL2', 'PA33', 'PA14', 'BT4', 'EX38', 'DL4', 'NN5', 'M90', 'EX5', 'BH24', 'SY15', 'DL10', 'IV10', 'WF16', 'CM6', 'AB45', 'BT11', 'KW16', 'PH33', 'IV11', 'G60', 'WV2', 'WV3', 'BA22', 'BB11', 'FY2', 'AB51', 'BT65', 'SG8', 'M30', 'DD7', 'PO5', 'SO18', 'PO39', 'EC1M', 'CF42', 'ME16', 'BT30', 'TR24', 'CV6', 'NE62', 'LN1', 'WD18', 'FY5', 'B5', 'B21', 'TR17', 'ST7', 'SA3', 'PH10', 'CH70', 'TW2', 'E7', 'S17', 'SW7', 'NE29', 'ML8', 'LL51', 'NG80', 'ME20', 'NG31', 'TR6', 'KA26', 'SM5', 'SW1H', 'NE21', 'PE33', 'LL61', 'FK8', 'IV54', 'CR0', 'PH50', 'NR24', 'KY6', 'DL16', 'S35', 'BS7', 'BT69', 'OX11', 'BD4', 'SG1', 'TN10', 'NP22', 'L5', 'WA15', 'BS31', 'OL2', 'L37', 'S13', 'DY3', 'AL10', 'OL9', 'PH39', 'LE19', 'FK21', 'DY7', 'PE34', 'MK40', 'SW4', 'PO21', 'NE63', 'L34', 'SA8', 'PL18', 'DH97', 'BB1', 'CV12', 'EN6', 'AB35', 'FK19', 'DY12', 'NR20', 'GU27', 'PL19', 'SW13', 'NR10', 'E9', 'BN44', 'SA37', 'OL1', 'SN13', 'BN25', 'DL14', 'IV30', 'YO61', 'SY7', 'LN13', 'KA16', 'PO15', 'PA23', 'CF34', 'HU5', 'AL1', 'L13', 'TN22', 'PO19', 'TS29', 'KA12', 'FY1', 'IV53', 'SE3', 'HA6', 'RM20', 'TA12', 'LL78', 'DD3', 'SE1P', 'WS4', 'HU14', 'EX22', 'KY99', 'G22', 'KA1', 'BT40', 'G2', 'FK1', 'TF4', 'WF11', 'M13', 'PA38', 'CH6', 'EH29', 'HX4', 'CR7', 'NE16', 'DG3', 'CT2', 'NR27', 'RG21', 'TQ8', 'BH8', 'L75', 'TW8', 'RM6', 'PE38', 'SW1W', 'EC1Y', 'BH14', 'NP11', 'IM3', 'E11', 'BS99', 'TQ11', 'WD5', 'SA47', 'LS16', 'G68', 'SL0', 'B3', 'PH3', 'BS15', 'CB9', 'BT32', 'NE38', 'IV2', 'DT2', 'PH21', 'WF10', 'TD11', 'PH22', 'YO10', 'G53', 'LL26', 'TN38', 'SL3', 'DY9', 'WF6', 'WA3', 'E2', 'CM8', 'OX14', 'BT54', 'SG16', 'G63', 'B43', 'IM9', 'BH18', 'W7', 'CM11', 'ME3', 'GU5', 'NE44', 'DY10', 'RH6', 'PL33', 'PA41', 'HU12', 'CH33', 'BN27', 'TS6', 'TD5', 'M50', 'NR22', 'LD6', 'SL8', 'EN11', 'IP6', 'PE21', 'S72', 'EX2', 'HP2', 'SK14', 'SE9', 'M40', 'WR3', 'DG9', 'IV14', 'GU14', 'RG26', 'L71', 'KT18', 'DT1', 'TS25', 'LL72', 'N4', 'NE24', 'BT18', 'BL7', 'NW4', 'M9', 'KW14', 'LA1', 'BT8', 'TR11', 'OX7', 'AL5', 'OL16', 'IV25', 'RG2', 'GL52', 'SP6', 'DA13', 'E1W', 'CV32', 'WS10', 'LS27', 'KA14', 'LL43', 'BT71', 'EC2N', 'RH3', 'B92', 'TD2', 'EC4Y', 'HP10', 'EH22', 'CV4', 'FK10', 'BT57', 'BA4', 'TF9', 'S33', 'BD21', 'KA13', 'G12', 'LN9', 'TR22', 'LN10', 'B45', 'N12', 'KT24', 'DE56', 'LU3', 'EH41', 'LN5', 'CW5', 'NE45', 'CV3', 'B50', 'TN37', 'YO15', 'TN30', 'LA21', 'postcode', 'HA7', 'LE10', 'CT18', 'GL16', 'DA8', 'PH36', 'CM98', 'BN91', 'CM21', 'UB3', 'CT21', 'FY6', 'TW15', 'NP44', 'LL49', 'WS6', 'L21', 'BT47', 'NR17', 'IV47', 'GL12', 'IP33', 'BT21', 'LL66', 'TA10', 'EH47', 'HR7', 'TD13', 'TA8', 'TW14', 'B9', 'WS14', 'BR3', 'S61', 'CT50', 'WA5', 'IV9', 'PO12', 'BT79', 'DH4', 'PO7', 'NW8', 'BD97', 'NG3', 'TS24', 'ST55', 'PA15', 'ME6', 'WA11', 'B34', 'TN8', 'LS26', 'BR1', 'BD8', 'NN9', 'KY1', 'IV44', 'DN38', 'NE17', 'LA4', 'CF31', 'BS32', 'TA18', 'B95', 'E10', 'IM1', 'DY11', 'IV27', 'DL1', 'HD7', 'B7', 'L30', 'LE55', 'EH21', 'NE6', 'CR3', 'TS22', 'ST12', 'PA10', 'TQ13', 'SE7', 'NE15', 'GY4', 'KA23', 'IG10', 'SG15', 'KA22', 'PE31', 'TS17', 'YO11', 'ST6', 'EX35', 'M41', 'LL20', 'M27', 'EX1', 'W13', 'S49', 'CM14', 'SW18', 'LL13', 'EH30', 'EX10', 'G78', 'DE72', 'W5', 'RH12', 'KT13', 'NG22', 'LN8', 'G58', 'GL51', 'LA2', 'SO25', 'KW13', 'LL15', 'PR0', 'GU46', 'TR27', 'PA46', 'LE4', 'EC3P', 'NE33', 'BT31', 'SO97']


    for element in outil:
        print(element)
        url = "https://www.zoopla.co.uk/for-sale/property/"+ element +"/?identifier=" + element + "&q=" + element + "&search_source=refine&radius=0&page_size=100&pn=0"
        agent = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        page = requests.get(url, headers=agent)
        try :
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                PAGE_LAST = int(re.findall("\d+", soup.find(class_="paginate bg-muted").get_text())[-1])
                BASE = "https://www.zoopla.co.uk/for-sale/property/"+ element +"/?identifier=" + element + "&q=" + element + "&search_source=refine&radius=0&page_size=100&pn="
                reqs = (grequests.get(BASE+str(i)) for i in range(PAGE_INIT, PAGE_LAST+1))
                pages = grequests.map(reqs)
                parse_parallel(pages)
            except:
                parse_page(page)
        except AttributeError:
            pass

# Parser les pages en parallèle
def parse_parallel(pages):
    for page in pages:
        # Ajout des tâches à la queue
        parse_page(page)

# Conversion vers un fichier CSV
def to_csv(p, filename):
    Type_bien = ["Appartement" if "flat" in dec.lower() else ("Maison" if "house" in dec.lower() else (
        "Terrain" if "land" in dec.lower() else ("Maisonette" if "maisonette" in dec.lower() else (
            "Studio" if "studio" in dec.lower() else ("Maison avec jardin" if "property" in dec.lower() else
            ("Bungalow" if "bungalow" in dec.lower() else ("Cottage" if "cottage" in dec.lower() else
            ("Duplex" if "duplex" in dec.lower() else ("Triplex" if "triplex" in dec.lower() else
            ("Garage/parking" if "garage" in dec.lower() else
            ("Mobilehome" if "mobile/park home" in dec.lower() else "NA")))))))))))
                for dec in p.description]

    codepostal_londres = ["E" + str(i) for i in range(30)] + ["EC" + str(i) for i in range(30)] + ["N" + str(i) for i in
                                                                                                   range(30)] + \
                         ["NW" + str(i) for i in range(30)] + ["SE" + str(i) for i in range(30)] + ["SW" + str(i) for i
                                                                                                    in range(30)] + \
                         ["W" + str(i) for i in range(30)] + ["WC" + str(i) for i in range(30)]

    codepostal_1 = [element[element.rfind(" ") + 1:] for element in p.adresses]

    county = ['bedfordshire', 'bedford', 'berkshire', 'berk', 'buckinghamshire', 'buckingham', 'cambridgeshire',
              'cambridge',
              'cheshire', 'chester', 'cornwall', 'cumberland', 'derbyshire', 'derby', 'devon', 'dorset', 'durham',
              'essex',
              'gloucestershire', 'gloucester', 'hampshire', 'southamptonshire', 'herefordshire', 'hereford',
              'hertfordshire', 'hertford',
              'huntingdonshire', 'huntingdon', 'kent', 'lancashire', 'lancaster', 'leicestershire', 'leicester',
              'lincolnshire',
              'lincoln', 'middlesex', 'norfolk', 'northamptonshire', 'northampton', 'northumberland', 'nottinghamshire',
              'nottingham', 'oxfordshire', 'oxford', 'rutland', 'shropshire', 'salop', 'somerset', 'somersetshire',
              'staffordshire',
              'stafford', 'suffolk', 'surrey', 'sussex', 'warwickshire', 'warwick', 'westmorland', 'wiltshire', 'wilt',
              'worcestershire',
              'worcester', 'yorkshire', 'york']

    Ville_1 = ["Londres" if element[element.rfind(" ") + 1:] in codepostal_londres else
               (element[element.find(",") + 2:element.rfind(",")] if element[element.rfind(",") + 2:element.rfind(
                   " ")].lower() in county
                else (element[element.rfind(",") + 2:element.rfind(" ")] if element[
                                                                            element.rfind(",") + 2:element.rfind(
                                                                                " ")] else "NA"))
               for element in p.adresses]

    Ville = [
        element[element.find(",") + 1:] if "," in element else ("NA" if element == '' else ("NA" if element == "." else
                                                        ("NA" if element == ' .' else element)))for element in Ville_1]

    adresses = [element.replace(",","") for element in p.adresses]

    codepostal = [element.replace(",","") for element in codepostal_1]

    Ville_final = [element.replace(",","") for element in Ville]

    immobiler_5 = pd.DataFrame({
        "URL" : p.les_urls,
        "ville" : Ville_final,
        "code postal" : codepostal,
        "Adresses": adresses,
        "prix livre" : p.prix,
        "surface m2": p.surfaces,
        "Enchere ou vente" : p.Auction,
        "Etat neuf ou ancien": p.Neuf_ou_ancien,
        "Nombre de chambres": p.nombre_de_chambre,
        "Nombre de SDB": p.nombre_de_SDB,
        "Nombre de séjour": p.nombre_de_sejour,
        "Description" : p.description,
        "Type bien" : Type_bien,
        "Aide" : p.Aide,
    })

    immobiler_5 = immobiler_5.drop_duplicates("URL",keep='last')
    immobiler_5.to_csv(filename)


load_pages()

# Writing the page into a CSV file
today = date.today()
to_csv(p, str(today) + ".csv")
print("duree=", time.time() - start_time)
print("requete non aboutie",requete_non_aboutie)