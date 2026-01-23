import AnimatedBurgerMenuCard from '@/components/AnimatedBurgerMenuCard'

export const metadata = {
  title: 'Burger Buiten - Menu',
  description: 'Ontdek ons heerlijke burger menu bij Burger Buiten',
}

export default function BurgerMenuPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 py-12">
      <AnimatedBurgerMenuCard />
    </main>
  )
}
