import Link from 'next/link'
import { ArrowRight, CheckCircle } from 'lucide-react'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Risk Management',
  description: 'Professioneel advies in risk management: risk appetite frameworks, ORSA/ICAAP begeleiding, three lines of defense en risk culture assessments.',
}

export default function RiskManagementPage() {
  const services = [
    'Risk appetite framework ontwikkeling',
    'ORSA/ICAAP begeleiding',
    'Three lines of defense implementatie',
    'Risk culture assessments',
    'Interimmanagement risk functie',
    'Risk governance opzet en verbetering',
  ]

  const targetGroups = [
    'Verzekeraars die hun risk framework willen versterken',
    'Beleggingsondernemingen met groeiende complexiteit',
    'Pensioenfondsen die voorbereiden op nieuwe wetgeving',
    'Scale-ups die een risk functie moeten opzetten',
  ]

  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <nav className="text-sm mb-4">
            <Link href="/diensten" className="text-gray-300 hover:text-white">Diensten</Link>
            <span className="mx-2">/</span>
            <span>Risk Management</span>
          </nav>
          <h1 className="text-4xl font-bold mb-4">Risk Management</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Effectief risk management gaat verder dan compliance. Het creëert waarde
            door betere besluitvorming en een sterker risicobewustzijn in de organisatie.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">De uitdaging</h2>
                <p className="text-gray-600">
                  Financiële instellingen worstelen vaak met het opzetten van effectieve
                  risk frameworks die niet alleen voldoen aan regelgeving, maar ook
                  daadwerkelijk waarde toevoegen aan de organisatie. Te vaak blijft risk
                  management een papieren exercitie die los staat van de dagelijkse praktijk.
                </p>
              </div>

              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Mijn aanpak</h2>
                <p className="text-gray-600 mb-6">
                  Met ervaring als toezichthouder én als Risk Officer begrijp ik wat
                  toezichthouders verwachten én wat praktisch haalbaar is. Mijn aanpak
                  is gericht op implementeerbare oplossingen die passen bij uw organisatie.
                </p>
                <ul className="space-y-3">
                  {services.map((service, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-6 w-6 text-primary-600 mr-3 flex-shrink-0" />
                      <span className="text-gray-700">{service}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Typische opdrachten</h2>
                <ul className="space-y-4 text-gray-600">
                  <li className="border-l-4 border-primary-600 pl-4">
                    Opzetten van een complete risk management functie bij een groeiende scale-up
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Second opinion op bestaande risk modellen en methodologie
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Voorbereiding op DNB on-site onderzoek: gap analyse en remediatie
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Training van RvC en directie in risk oversight en governance
                  </li>
                </ul>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-8">
              <div className="bg-gray-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Voor wie?</h3>
                <ul className="space-y-3">
                  {targetGroups.map((group, index) => (
                    <li key={index} className="text-gray-600 text-sm flex items-start">
                      <span className="w-2 h-2 bg-primary-600 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                      {group}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-primary-600 text-white p-6 rounded-xl">
                <h3 className="text-lg font-semibold mb-4">Interesse?</h3>
                <p className="text-gray-200 text-sm mb-6">
                  Bespreek uw specifieke situatie in een vrijblijvend kennismakingsgesprek.
                </p>
                <Link
                  href="/contact"
                  className="inline-flex items-center justify-center w-full px-4 py-3 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
                >
                  Neem contact op
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
