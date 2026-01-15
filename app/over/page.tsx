import Link from 'next/link'
import { ArrowRight, Briefcase, GraduationCap, Award } from 'lucide-react'
import { siteConfig } from '@/lib/constants'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Over',
  description: 'Ervaren professional met achtergrond bij De Nederlandsche Bank en expertise in risk management, actuariaat en compliance.',
}

export default function OverPage() {
  const expertise = [
    'Risk Management & Governance',
    'Actuariaat & Kapitaalberekeningen',
    'Solvency II & Toezicht',
    'Compliance & Regulatory Affairs',
    'ALM & Kapitaalmanagement',
    'Three Lines of Defense',
  ]

  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-4">Over mij</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Met meer dan 15 jaar ervaring in de financiële sector combineer ik
            diepgaande kennis van toezicht met praktische ervaring in risk management.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              {/* Bio */}
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-600 text-lg leading-relaxed">
                  Als toezichthouder Professional Finance bij <strong>De Nederlandsche Bank</strong> hield
                  ik toezicht op verzekeraars en pensioenfondsen, met focus op kapitaal- en
                  actuariële vraagstukken. Deze ervaring geeft mij uniek inzicht in wat
                  toezichthouders verwachten en hoe zij onderzoeken uitvoeren.
                </p>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Momenteel werk ik als <strong>Risk Officer</strong> bij een beleggingsonderneming,
                  waar ik dagelijks risk frameworks implementeer en onderhoud. Deze combinatie
                  van toezichtervaring en praktijkervaring stelt mij in staat om beide kanten
                  van de tafel te begrijpen.
                </p>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Daarnaast adviseer ik financiële instellingen die behoefte hebben aan
                  onafhankelijke expertise op het snijvlak van risk, actuariaat en compliance.
                  Mijn aanpak is praktisch, gericht op implementeerbare oplossingen die
                  passen bij uw specifieke situatie.
                </p>
              </div>

              {/* Timeline */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Carrière</h2>
                <div className="space-y-6">
                  {siteConfig.experience.map((exp, index) => (
                    <div key={index} className="flex gap-4">
                      <div className="flex-shrink-0">
                        <div className="w-12 h-12 bg-primary-600/10 rounded-full flex items-center justify-center">
                          <Briefcase className="h-6 w-6 text-primary-600" />
                        </div>
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{exp.role}</h3>
                        <p className="text-primary-600">{exp.company} • {exp.period}</p>
                        <p className="text-gray-600 mt-1">{exp.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Approach */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Mijn aanpak</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gray-50 p-6 rounded-xl">
                    <h3 className="font-semibold text-gray-900 mb-2">Praktisch</h3>
                    <p className="text-gray-600 text-sm">
                      Geen theoretische exercities, maar implementeerbare oplossingen
                      die passen bij uw organisatie en budget.
                    </p>
                  </div>
                  <div className="bg-gray-50 p-6 rounded-xl">
                    <h3 className="font-semibold text-gray-900 mb-2">Onafhankelijk</h3>
                    <p className="text-gray-600 text-sm">
                      Objectief advies zonder verborgen agenda of belangen bij
                      bepaalde producten of dienstverleners.
                    </p>
                  </div>
                  <div className="bg-gray-50 p-6 rounded-xl">
                    <h3 className="font-semibold text-gray-900 mb-2">Ervaren</h3>
                    <p className="text-gray-600 text-sm">
                      Meer dan 15 jaar ervaring aan beide kanten van de tafel:
                      toezicht én dagelijkse praktijk.
                    </p>
                  </div>
                  <div className="bg-gray-50 p-6 rounded-xl">
                    <h3 className="font-semibold text-gray-900 mb-2">Betrokken</h3>
                    <p className="text-gray-600 text-sm">
                      Ik werk nauw samen met uw team en zorg voor kennisoverdracht,
                      zodat u zelfstandig verder kunt.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-8">
              {/* Profile placeholder */}
              <div className="bg-gray-100 rounded-xl aspect-square flex items-center justify-center">
                <div className="text-center text-gray-400">
                  <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4"></div>
                  <p className="text-sm">Profielfoto</p>
                </div>
              </div>

              {/* Expertise */}
              <div className="bg-gray-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Expertise</h3>
                <div className="flex flex-wrap gap-2">
                  {expertise.map((item, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-primary-600/10 text-primary-600 text-sm rounded-full"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>

              {/* CTA */}
              <div className="bg-primary-600 text-white p-6 rounded-xl">
                <h3 className="text-lg font-semibold mb-4">Kennismaken?</h3>
                <p className="text-gray-200 text-sm mb-6">
                  Ik ga graag het gesprek aan over uw specifieke uitdagingen.
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
