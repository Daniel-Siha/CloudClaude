import Link from 'next/link'
import { ArrowRight, CheckCircle } from 'lucide-react'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Compliance & Toezicht',
  description: 'Compliance en toezicht expertise: DNB-onderzoeken, vergunningstrajecten, compliance frameworks en regulatory affairs.',
}

export default function ComplianceToezichtPage() {
  const services = [
    'Voorbereiding op DNB on-site onderzoeken',
    'Compliance framework opzet en verbetering',
    'Vergunningstrajecten (Wft, AIFMD, etc.)',
    'Regulatory gap analyses',
    'Training compliance en governance',
    'Interimmanagement compliance functie',
  ]

  const targetGroups = [
    'Financiële instellingen die een DNB-onderzoek verwachten',
    'Scale-ups die een vergunning aanvragen',
    'Organisaties die hun compliance framework willen versterken',
    'Partijen die een ervaren sparringpartner zoeken voor regulatory affairs',
  ]

  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <nav className="text-sm mb-4">
            <Link href="/diensten" className="text-gray-300 hover:text-white">Diensten</Link>
            <span className="mx-2">/</span>
            <span>Compliance & Toezicht</span>
          </nav>
          <h1 className="text-4xl font-bold mb-4">Compliance & Toezicht</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Als voormalig toezichthouder bij DNB weet ik precies waar toezichthouders
            naar kijken. Deze ervaring zet ik in om u optimaal voor te bereiden op
            toezichtonderzoeken en compliance-uitdagingen.
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
                  Toezicht op financiële instellingen wordt steeds intensiever. Een
                  DNB-onderzoek kan grote impact hebben op uw organisatie, zowel qua
                  tijdsbesteding als eventuele bevindingen. Goede voorbereiding en
                  een robuust compliance framework zijn essentieel.
                </p>
              </div>

              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Mijn aanpak</h2>
                <p className="text-gray-600 mb-6">
                  Door mijn ervaring als toezichthouder kan ik een uniek perspectief
                  bieden. Ik weet hoe onderzoeken worden opgezet, waar toezichthouders
                  naar kijken en hoe bevindingen tot stand komen. Dit stelt mij in staat
                  om u gericht voor te bereiden.
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
                    Mock-onderzoek ter voorbereiding op aankomend DNB bezoek
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Begeleiding vergunningaanvraag voor nieuwe beleggingsonderneming
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Gap analyse compliance framework tegen actuele regelgeving
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Training directie en medewerkers in omgang met toezichthouder
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
