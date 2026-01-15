import Link from 'next/link'
import { ArrowRight, CheckCircle } from 'lucide-react'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Actuariaat',
  description: 'Actuariële expertise: kapitaalberekeningen, technische voorzieningen, Solvency II analyses en second opinions.',
}

export default function ActuariaatPage() {
  const services = [
    'Actuariële analyses en berekeningen',
    'Kapitaalberekeningen (Solvency II, eigen modellen)',
    'Second opinion technische voorzieningen',
    'ALM-studies en scenario analyses',
    'Actuariële rapportages en SFCR ondersteuning',
    'Interimmanagement actuariële functie',
  ]

  const targetGroups = [
    'Verzekeraars met behoefte aan onafhankelijke actuariële expertise',
    'Pensioenfondsen die voorbereiden op het nieuwe pensioenstelsel',
    'Financiële instellingen met complexe verzekeringsverplichtingen',
    'Organisaties die een second opinion zoeken op actuariële aannames',
  ]

  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <nav className="text-sm mb-4">
            <Link href="/diensten" className="text-gray-300 hover:text-white">Diensten</Link>
            <span className="mx-2">/</span>
            <span>Actuariaat</span>
          </nav>
          <h1 className="text-4xl font-bold mb-4">Actuariaat</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Actuariële expertise is cruciaal voor het begrijpen en managen van
            langetermijnverplichtingen. Met een achtergrond in toezicht op kapitaal
            en actuariaat lever ik gedegen analyses.
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
                  Actuariële vraagstukken worden steeds complexer. Van Solvency II
                  kapitaalberekeningen tot de transitie naar het nieuwe pensioenstelsel:
                  de kwaliteit van actuariële analyses is bepalend voor strategische
                  beslissingen en toezichtrelaties.
                </p>
              </div>

              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Mijn aanpak</h2>
                <p className="text-gray-600 mb-6">
                  Als voormalig toezichthouder met focus op kapitaal en actuariaat
                  weet ik waar toezichthouders naar kijken. Dit stelt mij in staat
                  om actuariële analyses te leveren die niet alleen technisch correct
                  zijn, maar ook de toets van toezicht kunnen doorstaan.
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
                    Second opinion op best estimate berekeningen voor verzekeraar
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Ondersteuning bij transitie naar nieuw pensioenstelsel: doorrekenen scenarios
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Review van intern model voor Solvency II kapitaalberekening
                  </li>
                  <li className="border-l-4 border-primary-600 pl-4">
                    Opstellen actuarieel rapport en onderbouwing voor toezichthouder
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
