# Swedavia Flight Information

[🇸🇪 Läs på svenska](#svenska) | [Read in English](#english)

---

<a name="english"></a>
## 🇬🇧 English

Display flight information from Swedish Swedavia airports directly in Home Assistant!

### ⚠️ Important - API key required!

**Before installation:** You need a **free API key** from Swedavia:

1. Register at https://apideveloper.swedavia.se/
2. Subscribe to **FlightInfo** (free)
3. Copy your **Primary key** from Profile → Subscriptions

The key is required during integration setup.

### Features

- 🛬 **Arrivals** - Complete information about arriving flights including baggage information
- 🛫 **Departures** - Detailed information about departing flights with gate and check-in
- 🏢 **All Swedish airports** - Support for all 12 Swedavia airports
- 💼 **Baggage information** - See belt number and baggage times
- 🚪 **Gate details** - Terminal, gate, opening and closing times
- ⏰ **Flexible time window** - Customize how far forward/backward in time you want to see flights
- 🔄 **Automatic updates** - Data refreshed every 5 minutes from Swedavia's API

### Quick Start

1. Install via HACS
2. Go to Settings → Devices & Services
3. Add "Swedavia Flight Information"
4. Select airport and settings
5. Done! Your sensors are ready to use

### Swedish Airports

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

### Information Displayed

#### For arrivals
- Flight number (incl code-share)
- Airline
- Origin airport
- Scheduled, estimated and actual time
- Status (in Swedish)
- Terminal and gate
- **Baggage**: Belt number, first and last bag
- Remarks

#### For departures
- Flight number (incl code-share)
- Airline
- Destination airport
- Scheduled, estimated and actual time
- Status (in Swedish)
- Terminal and gate
- **Gate**: Action, opens/closes
- **Check-in**: Status, desk number
- Remarks

See README for complete examples of Lovelace cards and automations!

---

<a name="svenska"></a>
## 🇸🇪 Svenska

Visa flyginformation från svenska Swedavia-flygplatser direkt i Home Assistant!

### ⚠️ Viktigt - API-nyckel krävs!

**Innan installation:** Du måste skaffa en **gratis API-nyckel** från Swedavia:

1. Registrera på https://apideveloper.swedavia.se/
2. Prenumerera på **FlightInfo** (gratis)
3. Kopiera din **Primary key** från Profile → Subscriptions

Nyckeln behövs vid konfiguration av integrationen.

### Funktioner

- 🛬 **Ankomster** - Fullständig information om ankommande flyg inklusive bagage-information
- 🛫 **Avgångar** - Detaljerad information om avgående flyg med gate och incheckning
- 🏢 **Alla svenska flygplatser** - Stöd för alla 12 Swedavia-flygplatser
- 💼 **Bagageinformation** - Se band-nummer och tider för bagage
- 🚪 **Gate-detaljer** - Terminal, gate, öppnings- och stängningstider
- ⏰ **Flexibelt tidsfönster** - Anpassa hur långt fram/tillbaka i tiden du vill se flyg
- 🔄 **Automatisk uppdatering** - Data uppdateras var 5:e minut från Swedavias API

### Snabbstart

1. Installera via HACS
2. Gå till Inställningar → Enheter & tjänster
3. Lägg till "Swedavia Flight Information"
4. Välj flygplats och inställningar
5. Klart! Dina sensorer är redo att användas

### Svenska flygplatser

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

### Information som visas

#### För ankomster
- Flightnummer (inkl code-share)
- Flygbolag
- Ursprungsflygplats
- Schemalagd, beräknad och faktisk tid
- Status på svenska
- Terminal och gate
- **Bagage**: Band-nummer, första och sista väska
- Anmärkningar

#### För avgångar
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
