# Swedavia Flight Information

Visa flyginformation från svenska Swedavia-flygplatser direkt i Home Assistant!

## ⚠️ Viktigt - API-nyckel krävs!

**Innan installation:** Du måste skaffa en **gratis API-nyckel** från Swedavia:

1. Registrera på https://apideveloper.swedavia.se/
2. Prenumerera på **FlightInfo** (gratis)
3. Kopiera din **Primary key** från Profile → Subscriptions

Nyckeln behövs vid konfiguration av integrationen.

## Funktioner

- 🛬 **Ankomster** - Fullständig information om ankommande flyg inklusive bagage-information
- 🛫 **Avgångar** - Detaljerad information om avgående flyg med gate och incheckning
- 🏢 **Alla svenska flygplatser** - Stöd för alla 12 Swedavia-flygplatser
- 💼 **Bagageinformation** - Se band-nummer och tider för bagage
- 🚪 **Gate-detaljer** - Terminal, gate, öppnings- och stängningstider
- ⏰ **Flexibelt tidsfönster** - Anpassa hur långt fram/tillbaka i tiden du vill se flyg
- 🔄 **Automatisk uppdatering** - Data uppdateras var 5:e minut från Swedavias API

## Snabbstart

1. Installera via HACS
2. Gå till Inställningar → Enheter & tjänster
3. Lägg till "Swedavia Flight Information"
4. Välj flygplats och inställningar
5. Klart! Dina sensorer är redo att användas

## Svenska flygplatser

- Stockholm Arlanda (ARN)
- Stockholm Bromma (BMA)  
- Göteborg Landvetter (GOT)
- Malmö (MMX)
- Luleå (LLA)
- Umeå (UME)
- Visby (VBY)
- Kiruna (KRN)
- Ronneby (RNB)
- Stockholm Västerås (VST)
- Örebro (ORB)
- Stockholm Skavsta (NYO)

## Information som visas

### För ankomster
- Flightnummer (inkl code-share)
- Flygbolag
- Ursprungsflygplats
- Schemalagd, beräknad och faktisk tid
- Status på svenska
- Terminal och gate
- **Bagage**: Band-nummer, första och sista väska
- Anmärkningar

### För avgångar
- Flightnummer (inkl code-share)
- Flygbolag
- Destinationsflygplats
- Schemalagd, beräknad och faktisk tid
- Status på svenska
- Terminal och gate
- **Gate**: Åtgärd, öppnar/stänger
- **Incheckning**: Status, disk-nummer
- Anmärkningar

Se README för fullständiga exempel på Lovelace-kort och automationer!
