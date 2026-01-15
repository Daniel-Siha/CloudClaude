import { siteConfig } from '@/lib/constants'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Privacy',
  description: 'Privacyverklaring en informatie over gegevensverwerking.',
}

export default function PrivacyPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-4">Privacyverklaring</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Hoe ik omga met uw persoonsgegevens.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          <div className="prose prose-lg max-w-none">
            <h2>1. Wie ben ik?</h2>
            <p>
              {siteConfig.name} is verantwoordelijk voor de verwerking van persoonsgegevens
              zoals weergegeven in deze privacyverklaring.
            </p>
            <p>
              <strong>Contactgegevens:</strong><br />
              E-mail: {siteConfig.contact.email}<br />
              KvK: {siteConfig.contact.kvk}
            </p>

            <h2>2. Welke persoonsgegevens verwerk ik?</h2>
            <p>
              Ik verwerk persoonsgegevens doordat u gebruik maakt van mijn diensten
              en/of omdat u deze zelf aan mij verstrekt. Hieronder vindt u een
              overzicht van de persoonsgegevens die ik verwerk:
            </p>
            <ul>
              <li>Voor- en achternaam</li>
              <li>E-mailadres</li>
              <li>Organisatienaam</li>
              <li>Inhoud van uw bericht via het contactformulier</li>
            </ul>

            <h2>3. Met welk doel verwerk ik persoonsgegevens?</h2>
            <p>Ik verwerk uw persoonsgegevens voor de volgende doelen:</p>
            <ul>
              <li>Om contact met u op te kunnen nemen naar aanleiding van uw vraag</li>
              <li>Om mijn dienstverlening te kunnen uitvoeren</li>
              <li>Om u te informeren over wijzigingen in mijn diensten</li>
            </ul>

            <h2>4. Hoe lang bewaar ik persoonsgegevens?</h2>
            <p>
              Ik bewaar uw persoonsgegevens niet langer dan strikt nodig is om de
              doelen te realiseren waarvoor uw gegevens worden verzameld. Contactgegevens
              worden maximaal 2 jaar na het laatste contact bewaard.
            </p>

            <h2>5. Delen van persoonsgegevens met derden</h2>
            <p>
              Ik verstrek geen persoonsgegevens aan derden, tenzij dit noodzakelijk
              is voor de uitvoering van mijn dienstverlening of om te voldoen aan
              een wettelijke verplichting.
            </p>

            <h2>6. Cookies</h2>
            <p>
              Deze website maakt geen gebruik van tracking cookies. Eventuele
              functionele cookies zijn uitsluitend noodzakelijk voor de werking
              van de website.
            </p>

            <h2>7. Gegevens inzien, aanpassen of verwijderen</h2>
            <p>
              U heeft het recht om uw persoonsgegevens in te zien, te corrigeren
              of te verwijderen. Daarnaast heeft u het recht om uw eventuele
              toestemming voor de gegevensverwerking in te trekken of bezwaar
              te maken tegen de verwerking van uw persoonsgegevens.
            </p>
            <p>
              U kunt een verzoek tot inzage, correctie, verwijdering of
              gegevensoverdraging van uw persoonsgegevens sturen naar{' '}
              {siteConfig.contact.email}.
            </p>

            <h2>8. Beveiliging</h2>
            <p>
              Ik neem de bescherming van uw gegevens serieus en neem passende
              maatregelen om misbruik, verlies, onbevoegde toegang, ongewenste
              openbaarmaking en ongeoorloofde wijziging tegen te gaan.
            </p>

            <h2>9. Klachten</h2>
            <p>
              Als u een klacht heeft over de verwerking van uw persoonsgegevens,
              neem dan contact met mij op. Komt u er samen met mij niet uit, dan
              heeft u altijd het recht een klacht in te dienen bij de Autoriteit
              Persoonsgegevens.
            </p>

            <hr />

            <h2>Disclaimer</h2>
            <p>
              De informatie op deze website is algemeen van aard en kan niet worden
              beschouwd als professioneel advies. Voor specifieke situaties dient
              altijd deskundig advies te worden ingewonnen.
            </p>
            <p>
              {siteConfig.name} aanvaardt geen aansprakelijkheid voor schade die
              voortvloeit uit het gebruik van informatie op deze website.
            </p>

            <p className="text-sm text-gray-500 mt-8">
              Laatste update: januari 2026
            </p>
          </div>
        </div>
      </section>
    </>
  )
}
