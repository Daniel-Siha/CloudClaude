import Link from 'next/link'
import { Shield, Calculator, FileCheck, TrendingUp, ArrowRight } from 'lucide-react'
import { siteConfig } from '@/lib/constants'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Diensten',
  description: 'Onafhankelijk advies in risk management, actuariaat, compliance en kapitaalmanagement voor financiële instellingen.',
}

const iconMap = {
  Shield,
  Calculator,
  FileCheck,
  TrendingUp,
}

export default function DienstenPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-4">Diensten</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Onafhankelijk advies op het snijvlak van risk, actuariaat en compliance.
            Met ervaring aan beide kanten van de tafel help ik financiële instellingen
            hun doelen te bereiken.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {siteConfig.services.map((service) => {
              const Icon = iconMap[service.icon as keyof typeof iconMap]
              return (
                <Link
                  key={service.title}
                  href={service.href}
                  className="bg-white border border-gray-200 p-8 rounded-xl hover:border-primary-600 hover:shadow-lg transition-all group"
                >
                  <div className="flex items-start gap-4">
                    <div className="w-14 h-14 bg-primary-600/10 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-primary-600 transition-colors">
                      <Icon className="h-7 w-7 text-primary-600 group-hover:text-white transition-colors" />
                    </div>
                    <div className="flex-1">
                      <h2 className="text-xl font-semibold text-gray-900 mb-2 flex items-center">
                        {service.title}
                        <ArrowRight className="ml-2 h-5 w-5 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                      </h2>
                      <p className="text-gray-600">{service.description}</p>
                    </div>
                  </div>
                </Link>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gray-50 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Niet zeker welke dienst u nodig heeft?
          </h2>
          <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
            Plan een vrijblijvend kennismakingsgesprek en bespreek uw specifieke situatie.
          </p>
          <Link
            href="/contact"
            className="inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
          >
            Neem contact op
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>
    </>
  )
}
