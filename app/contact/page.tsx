import { Mail, Linkedin, MapPin } from 'lucide-react'
import { siteConfig } from '@/lib/constants'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Contact',
  description: 'Neem contact op voor een vrijblijvend kennismakingsgesprek over risk management, actuariaat of compliance.',
}

export default function ContactPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-primary-600 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-4">Contact</h1>
          <p className="text-xl text-gray-200 max-w-3xl">
            Heeft u vragen of wilt u kennismaken? Neem gerust contact op voor
            een vrijblijvend gesprek.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Stuur een bericht</h2>
              <form className="space-y-6" action={`mailto:${siteConfig.contact.email}`} method="POST" encType="text/plain">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                    Naam *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent outline-none transition-shadow"
                    placeholder="Uw naam"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    E-mail *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent outline-none transition-shadow"
                    placeholder="uw@email.nl"
                  />
                </div>

                <div>
                  <label htmlFor="organization" className="block text-sm font-medium text-gray-700 mb-2">
                    Organisatie
                  </label>
                  <input
                    type="text"
                    id="organization"
                    name="organization"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent outline-none transition-shadow"
                    placeholder="Naam van uw organisatie"
                  />
                </div>

                <div>
                  <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
                    Onderwerp *
                  </label>
                  <select
                    id="subject"
                    name="subject"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent outline-none transition-shadow"
                  >
                    <option value="">Selecteer een onderwerp</option>
                    <option value="risk-management">Risk Management</option>
                    <option value="actuariaat">Actuariaat</option>
                    <option value="compliance">Compliance & Toezicht</option>
                    <option value="kapitaalmanagement">Kapitaalmanagement</option>
                    <option value="kennismaking">Algemene kennismaking</option>
                    <option value="anders">Anders</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                    Bericht *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={5}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-transparent outline-none transition-shadow resize-none"
                    placeholder="Uw bericht..."
                  ></textarea>
                </div>

                <button
                  type="submit"
                  className="w-full px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Verstuur bericht
                </button>
              </form>
            </div>

            {/* Contact Info */}
            <div className="space-y-8">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Contactgegevens</h2>
                <div className="space-y-6">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary-600/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Mail className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">E-mail</h3>
                      <a
                        href={`mailto:${siteConfig.contact.email}`}
                        className="text-primary-600 hover:underline"
                      >
                        {siteConfig.contact.email}
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary-600/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Linkedin className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">LinkedIn</h3>
                      <a
                        href={siteConfig.contact.linkedin}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:underline"
                      >
                        Bekijk profiel
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-primary-600/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <MapPin className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">KvK</h3>
                      <p className="text-gray-600">{siteConfig.contact.kvk}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* FAQ */}
              <div className="bg-gray-50 p-6 rounded-xl">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Veelgestelde vragen</h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900">Wat kost een kennismakingsgesprek?</h4>
                    <p className="text-gray-600 text-sm mt-1">
                      Een eerste kennismakingsgesprek is altijd vrijblijvend en kosteloos.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Hoe snel kan ik starten?</h4>
                    <p className="text-gray-600 text-sm mt-1">
                      Afhankelijk van de opdracht kan ik vaak binnen een week starten.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Werkt u ook op interim basis?</h4>
                    <p className="text-gray-600 text-sm mt-1">
                      Ja, ik ben beschikbaar voor zowel projectmatig werk als interim opdrachten.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
