export const siteConfig = {
  name: 'Risk & Compliance Advisory',
  description: 'Onafhankelijk advies in risk management, actuariaat en compliance voor financiële instellingen',
  tagline: 'Van toezichthouder tot trusted advisor',
  contact: {
    email: 'info@example.nl',
    linkedin: 'https://linkedin.com/in/example',
    kvk: '12345678',
  },
  navigation: [
    { name: 'Home', href: '/' },
    { name: 'Diensten', href: '/diensten' },
    { name: 'Over', href: '/over' },
    { name: 'Contact', href: '/contact' },
  ],
  services: [
    {
      title: 'Risk Management',
      description: 'Opzetten en verbeteren van risk frameworks, ORSA/ICAAP begeleiding en risk culture assessments.',
      href: '/diensten/risk-management',
      icon: 'Shield',
    },
    {
      title: 'Actuariaat',
      description: 'Actuariële analyses, kapitaalberekeningen en second opinions op technische voorzieningen.',
      href: '/diensten/actuariaat',
      icon: 'Calculator',
    },
    {
      title: 'Compliance & Toezicht',
      description: 'Voorbereiding op DNB-onderzoeken, compliance frameworks en vergunningstrajecten.',
      href: '/diensten/compliance-toezicht',
      icon: 'FileCheck',
    },
    {
      title: 'Kapitaalmanagement',
      description: 'Solvency II optimalisatie, kapitaalplanning en ALM-vraagstukken.',
      href: '/diensten/kapitaalmanagement',
      icon: 'TrendingUp',
    },
  ],
  experience: [
    {
      role: 'Risk Officer',
      company: 'Beleggingsonderneming',
      period: 'Heden',
      description: 'Verantwoordelijk voor risk management framework en compliance',
    },
    {
      role: 'Toezichthouder Professional Finance',
      company: 'De Nederlandsche Bank',
      period: 'Voorgaand',
      description: 'Toezicht op verzekeraars en pensioenfondsen, focus op kapitaal en actuariaat',
    },
  ],
}
