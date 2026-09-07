import pandas as pd

dataframe = pd.read_csv("C:\\Users\\39339\\Desktop\\dataset\\archive\\digital_marketing_campaign.csv")

pd.set_option('display.float_format', lambda x: '%.2f' % x)

# 1. SEGMENTAZIONE DEMOGRAFICA
# Creazione di fasce d'età per analizzare il reddito medio e le conversioni
dataframe['AgeGroup'] = pd.cut(dataframe['Age'], bins=[18, 30, 45, 60, 100], labels=['18-30', '31-45', '46-60', '60+'])

demografiche = dataframe.groupby(['AgeGroup', 'Gender']).agg(
    Reddito_Medio=('Income', 'mean'),
    Tasso_Conversione=('Conversion', 'mean'),
    Totale_Clienti=('CustomerID', 'count')
).reset_index()


# 2. EFFICACIA CANALI E CAMPAGNE
# Performance medie e totali divise per Canale di Marketing
canali = dataframe.groupby('CampaignChannel').agg(
    Spesa_Totale=('AdSpend', 'sum'),
    CTR_Medio=('ClickThroughRate', 'mean'),
    ConversionRate_Medio=('ConversionRate', 'mean'),
    Conversioni_Totali=('Conversion', 'sum')
).reset_index()

# ROI approssimativo: Costo per Conversione (AdSpend / Conversioni Totali)
canali['Costo_Per_Conversione'] = canali['Spesa_Totale'] / canali['Conversioni_Totali']


# 3. COMPORTAMENTO SUL SITO
# Correlazione tra metriche di navigazione e conversione
metriche_sito = ['WebsiteVisits', 'PagesPerVisit', 'TimeOnSite', 'SocialShares', 'Conversion']
correlazione_sito = dataframe[metriche_sito].corr()['Conversion'].sort_values(ascending=False)

# Confronto diretto tra chi ha convertito (1) e chi no (0)
comportamento_utenti = dataframe.groupby('Conversion').agg(
    Tempo_Medio_Sito=('TimeOnSite', 'mean'),
    Pagine_Medie=('PagesPerVisit', 'mean'),
    Visite_Medie=('WebsiteVisits', 'mean'),
    Email_Aperte=('EmailOpens', 'mean')
).reset_index()


# 4. FEDELTÀ E RETENTION
# Analisi dei punti fedeltà e acquisti precedenti rispetto alle campagne di Retention
retention_df = dataframe[dataframe['CampaignType'] == 'Retention']

fedelta = retention_df.groupby('Conversion').agg(
    Acquisti_Precedenti_Medi=('PreviousPurchases', 'mean'),
    Punti_Fedelta_Medi=('LoyaltyPoints', 'mean')
).reset_index()



# Stampa completa di tutte le metriche calcolate

print("=== 1. SEGMENTAZIONE DEMOGRAFICA ===")
print(demografiche.round(2).to_string(index=False))

print("\n=== 2. PERFORMANCE CANALI DI MARKETING ===")
print(canali.round(2).to_string(index=False))

print("\n=== 3A. CORRELAZIONE TRA METRICHE SITO E CONVERSIONE ===")
print(correlazione_sito.round(2).to_string())

print("\n=== 3B. COMPORTAMENTO UTENTI (CONVERTITI VS NON CONVERTITI) ===")
print(comportamento_utenti.round(2).to_string(index=False))

print("\n=== 4. IMPATTO FEDELTÀ NELLE CAMPAGNE DI RETENTION ===")
print(fedelta.round(2).to_string(index=False))

# Esportazione in un unico file Excel con più fogli
with pd.ExcelWriter('report_analisi_marketing.xlsx') as writer:
    demografiche.round(2).to_excel(writer, sheet_name='Demografia', index=False)
    canali.round(2).to_excel(writer, sheet_name='Canali Marketing', index=False)
    comportamento_utenti.round(2).to_excel(writer, sheet_name='Comportamento Sito', index=False)
    fedelta.round(2).to_excel(writer, sheet_name='Retention e Fedelta', index=False)

print("\nReport salvato con successo in 'report_analisi_marketing.xlsx'!")