import Link from 'next/link'
import { Shield, Calculator, FileCheck, TrendingUp, ArrowRight } from 'lucide-react'
import { siteConfig } from '@/lib/constants'

const iconMap = {
  Shield,
  Calculator,
  FileCheck,
  TrendingUp,
}

export default function Home() {
  return (
    <>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="max-w-3xl">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              {siteConfig.tagline}
            </h1>
            <p className="text-xl text-gray-200 mb-8">
              Als voormalig toezichthouder bij De Nederlandsche Bank en huidig Risk Officer
              begrijp ik beide kanten van de tafel. Ik help financiële instellingen met
              risk management, actuariële vraagstukken en compliance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/contact"
                className="inline-flex items-center justify-center px-6 py-3 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
              >
                Neem contact op
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                href="/diensten"
                className="inline-flex items-center justify-center px-6 py-3 border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition-colors"
              >
                Bekijk diensten
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Diensten</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Onafhankelijk advies op het snijvlak van risk, actuariaat en compliance
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {siteConfig.services.map((service) => {
              const Icon = iconMap[service.icon as keyof typeof iconMap]
              return (
                <Link
                  key={service.title}
                  href={service.href}
                  className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow group"
                >
                  <div className="w-12 h-12 bg-primary-600/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary-600/20 transition-colors">
                    <Icon className="h-6 w-6 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {service.title}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {service.description}
                  </p>
                </Link>
              )
            })}
          </div>
        </div>
      </section>

      {/* Experience Section */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">
                Ervaring & Achtergrond
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Met meer dan 15 jaar ervaring in de financiële sector combineer ik
                diepgaande kennis van toezicht met praktische ervaring in risk management.
              </p>
              <div className="space-y-6">
                {siteConfig.experience.map((exp, index) => (
                  <div key={index} className="border-l-4 border-primary-600 pl-4">
                    <h3 className="font-semibold text-gray-900">{exp.role}</h3>
                    <p className="text-primary-600 text-sm">{exp.company} • {exp.period}</p>
                    <p className="text-gray-600 text-sm mt-1">{exp.description}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gray-100 rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Waarom kiezen voor mij?</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">1</span>
                  <span className="text-gray-700">Uniek perspectief door ervaring aan beide kanten van de tafel</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">2</span>
                  <span className="text-gray-700">Diepgaande kennis van DNB-toezicht en verwachtingen</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">3</span>
                  <span className="text-gray-700">Praktische aanpak gericht op implementeerbare oplossingen</span>
                </li>
                <li className="flex items-start">
                  <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">4</span>
                  <span className="text-gray-700">Onafhankelijk en objectief advies zonder verborgen agenda</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Klaar om uw risk management naar een hoger niveau te tillen?
          </h2>
          <p className="text-xl text-gray-200 mb-8 max-w-2xl mx-auto">
            Plan een vrijblijvend kennismakingsgesprek en ontdek hoe ik u kan helpen.
          </p>
          <Link
            href="/contact"
            className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors text-lg"
          >
            Plan een gesprek
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>
    </>
  )
}
