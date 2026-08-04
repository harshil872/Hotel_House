import os
import sys
import urllib.request
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hotel_House.settings')
django.setup()

from django.core.files.base import ContentFile
from User_Dashboard.models import MenuCategory, MenuItem, GalleryImage, TeamMember, Testimonial

print("Starting restaurant database seeding...")

# Helper to download image safely
def get_image_file(url, filename):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return ContentFile(response.read(), name=filename)
    except Exception as e:
        print(f"Warning: Failed to download {url}: {e}")
        return None

# 1. Clear old data
MenuItem.objects.all().delete()
MenuCategory.objects.all().delete()
GalleryImage.objects.all().delete()
TeamMember.objects.all().delete()
Testimonial.objects.all().delete()

# 2. Create Categories
cat_starters = MenuCategory.objects.create(
    name="Starters & Appetizers",
    slug="starters",
    description="Delicate bites and artfully crafted starters to ignite your palate.",
    icon="fa-concierge-bell",
    order=1
)

cat_mains = MenuCategory.objects.create(
    name="Chef's Signature Mains",
    slug="mains",
    description="Exquisite main courses featuring prime cuts, organic poultry, and seasonal produce.",
    icon="fa-utensils",
    order=2
)

cat_seafood = MenuCategory.objects.create(
    name="Seafood & Ocean Delicacies",
    slug="seafood",
    description="Sustainably wild-caught ocean treasures prepared with French and Japanese techniques.",
    icon="fa-fish",
    order=3
)

cat_desserts = MenuCategory.objects.create(
    name="Artisanal Desserts",
    slug="desserts",
    description="Decadent confections, house-spun gelatos, and warm pastries.",
    icon="fa-cookie-bite",
    order=4
)

cat_beverages = MenuCategory.objects.create(
    name="Sommelier Cellar & Cocktails",
    slug="beverages",
    description="Curated vintage wines, reserve champagnes, and handcrafted botanical cocktails.",
    icon="fa-glass-martini-alt",
    order=5
)

print("Categories created.")

# 3. Create Menu Items
dishes_data = [
    # Starters
    {
        'category': cat_starters,
        'name': 'French Onion Soup Gratinée',
        'description': 'Rich 24-hour caramelized onion broth, aged Gruyère crust, sourdough crouton, fresh thyme.',
        'price': 22.00,
        'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&auto=format&fit=crop&q=80',
        'filename': 'french_onion.jpg',
        'spice_level': 'none',
        'is_vegetarian': True,
        'is_featured': True,
        'ingredients': 'Caramelized Onions, Gruyère Cheese, Beef Broth, Sourdough, Thyme, Cognac',
        'prep_time': 15,
        'calories': 410,
        'chef_notes': 'Pair with a crisp Chablis or light Burgundy Pinot Noir.',
        'order': 1,
    },
    {
        'category': cat_starters,
        'name': 'Heirloom Tomato & Burrata Tartine',
        'description': 'Sun-ripened organic heirloom tomatoes, creamy Pugliese burrata, 25-year aged Modena balsamic, micro basil.',
        'price': 24.00,
        'image_url': 'https://images.unsplash.com/photo-1541529086526-db283c563270?w=800&auto=format&fit=crop&q=80',
        'filename': 'burrata_tartine.jpg',
        'spice_level': 'none',
        'is_vegetarian': True,
        'is_gluten_free': False,
        'is_featured': False,
        'ingredients': 'Heirloom Tomatoes, Burrata, Balsamic Glaze, Extra Virgin Olive Oil, Basil',
        'prep_time': 12,
        'calories': 380,
        'chef_notes': 'Best enjoyed alongside our house sourdough.',
        'order': 2,
    },
    {
        'category': cat_starters,
        'name': 'Yellowtail Kingfish Crudo',
        'description': 'Thinly sliced wild Pacific yellowtail, yuzu kosho vinaigrette, pickled radishes, finger lime caviar.',
        'price': 28.00,
        'image_url': 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800&auto=format&fit=crop&q=80',
        'filename': 'yellowtail_crudo.jpg',
        'spice_level': 'mild',
        'is_gluten_free': True,
        'is_featured': True,
        'ingredients': 'Pacific Yellowtail, Yuzu Kosho, Finger Lime, Radish, Shiso Leaves, Sesame Oil',
        'prep_time': 10,
        'calories': 290,
        'chef_notes': 'An ethereal starter that pairs beautifully with vintage Champagne.',
        'order': 3,
    },

    # Mains
    {
        'category': cat_mains,
        'name': 'A5 Miyazaki Wagyu Tenderloin',
        'description': 'Seared A5 Wagyu beef, truffle-infused pomme purée, braised baby carrots, bone marrow jus.',
        'price': 95.00,
        'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&auto=format&fit=crop&q=80',
        'filename': 'wagyu_steak.jpg',
        'spice_level': 'none',
        'is_gluten_free': True,
        'is_featured': True,
        'ingredients': 'A5 Wagyu Beef, Périgord Truffle, Butter, Potatoes, Bone Marrow Demi-Glace',
        'prep_time': 25,
        'calories': 780,
        'chef_notes': 'Our crown jewel dish. Perfectly paired with a full-bodied Cabernet Sauvignon.',
        'order': 1,
    },
    {
        'category': cat_mains,
        'name': 'Périgord Black Truffle Tagliolini',
        'description': 'Hand-rolled egg pasta, 36-month aged Parmigiano Reggiano crema, freshly shaved French black truffle.',
        'price': 46.00,
        'image_url': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800&auto=format&fit=crop&q=80',
        'filename': 'truffle_pasta.jpg',
        'spice_level': 'none',
        'is_vegetarian': True,
        'is_featured': True,
        'ingredients': 'Fresh Tagliolini Pasta, Périgord Black Truffle, Parmigiano Reggiano, Normandy Butter',
        'prep_time': 18,
        'calories': 620,
        'chef_notes': 'Truffles are shaved tableside by your captain.',
        'order': 2,
    },
    {
        'category': cat_mains,
        'name': 'Duck Breast à l\'Orange & Lavender',
        'description': 'Pan-roasted Moulard duck breast, blood orange glaze, lavender honey, roasted heirloom carrots.',
        'price': 48.00,
        'image_url': 'https://images.unsplash.com/photo-1514944288352-fffac99f0bdf?w=800&auto=format&fit=crop&q=80',
        'filename': 'duck_breast.jpg',
        'spice_level': 'none',
        'is_gluten_free': True,
        'is_featured': False,
        'ingredients': 'Moulard Duck, Blood Orange, Provençal Lavender Honey, Glazed Carrots, Thyme',
        'prep_time': 22,
        'calories': 650,
        'chef_notes': 'Cooked medium-rare to preserve maximum tenderness and flavor.',
        'order': 3,
    },

    # Seafood
    {
        'category': cat_seafood,
        'name': 'Butter-Poached Maine Lobster Tail',
        'description': 'Sweet Maine lobster poached in cultured butter, saffron risotto, sea asparagus, Oscietra caviar.',
        'price': 78.00,
        'image_url': 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800&auto=format&fit=crop&q=80',
        'filename': 'maine_lobster.jpg',
        'spice_level': 'none',
        'is_gluten_free': True,
        'is_featured': True,
        'ingredients': 'Maine Lobster Tail, Acquerello Rice, Spanish Saffron, Butter, Oscietra Caviar',
        'prep_time': 20,
        'calories': 590,
        'chef_notes': 'Finished with a touch of Meyer lemon zest for brightness.',
        'order': 1,
    },
    {
        'category': cat_seafood,
        'name': 'Pan-Seared Wild King Salmon',
        'description': 'Crispy skin Alaskan King Salmon, dill velouté, asparagus spears, crushed Yukon gold potatoes.',
        'price': 42.00,
        'image_url': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=800&auto=format&fit=crop&q=80',
        'filename': 'king_salmon.jpg',
        'spice_level': 'none',
        'is_gluten_free': True,
        'is_featured': False,
        'ingredients': 'Alaskan King Salmon, Fresh Dill, Shallots, White Wine, Cream, Asparagus',
        'prep_time': 18,
        'calories': 520,
        'chef_notes': 'Sourced from sustainable wild Alaskan fisheries.',
        'order': 2,
    },

    # Desserts
    {
        'category': cat_desserts,
        'name': 'Tahitian Vanilla Bean Crème Brûlée',
        'description': 'Silky custard infused with whole Tahitian vanilla beans, crisp caramelized sugar crust, fresh raspberries.',
        'price': 18.00,
        'image_url': 'https://images.unsplash.com/photo-1470124182917-cc6e71b22ecc?w=800&auto=format&fit=crop&q=80',
        'filename': 'creme_brulee.jpg',
        'spice_level': 'none',
        'is_vegetarian': True,
        'is_gluten_free': True,
        'is_featured': True,
        'ingredients': 'Heavy Cream, Egg Yolks, Tahitian Vanilla Bean, Turbinado Sugar, Raspberries',
        'prep_time': 10,
        'calories': 420,
        'chef_notes': 'Torched to order for the perfect crackling crust.',
        'order': 1,
    },
    {
        'category': cat_desserts,
        'name': 'Warm Valrhona Chocolate Soufflé',
        'description': '70% Valrhona dark chocolate soufflé, molten center, house-spun pistachios ice cream.',
        'price': 22.00,
        'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800&auto=format&fit=crop&q=80',
        'filename': 'chocolate_souffle.jpg',
        'spice_level': 'none',
        'is_vegetarian': True,
        'is_featured': True,
        'ingredients': 'Valrhona 70% Chocolate, Farm Eggs, Butter, Cocoa Powder, Pistachio Ice Cream',
        'prep_time': 20,
        'calories': 510,
        'chef_notes': 'Baked fresh to order. Please allow 20 minutes preparation time.',
        'order': 2,
    },

    # Beverages
    {
        'category': cat_beverages,
        'name': 'Smoked Old Fashioned Reserve',
        'description': 'WhistlePig 10-Yr Rye Bourbon, house aromatic bitters, smoked applewood, expressed orange peel.',
        'price': 24.00,
        'image_url': 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&auto=format&fit=crop&q=80',
        'filename': 'old_fashioned.jpg',
        'spice_level': 'none',
        'is_vegan': True,
        'is_gluten_free': True,
        'is_featured': True,
        'ingredients': 'WhistlePig Rye Bourbon, Angostura Bitters, Demerara Sugar, Applewood Smoke',
        'prep_time': 5,
        'calories': 180,
        'chef_notes': 'Served over a hand-carved crystal ice sphere.',
        'order': 1,
    },
    {
        'category': cat_beverages,
        'name': 'Château Margaux Premier Grand Cru 2015',
        'description': 'Legendary Bordeaux vintage. Complex notes of blackcurrant, cedar wood, violet, and graphite.',
        'price': 350.00,
        'image_url': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&auto=format&fit=crop&q=80',
        'filename': 'chateau_margaux.jpg',
        'spice_level': 'none',
        'is_vegan': True,
        'is_gluten_free': True,
        'is_featured': False,
        'ingredients': '87% Cabernet Sauvignon, 8% Merlot, 3% Cabernet Franc, 2% Petit Verdot',
        'prep_time': 5,
        'calories': 150,
        'chef_notes': 'Decanted 45 minutes prior to pouring for peak aromatic expressiveness.',
        'order': 2,
    },
]

for d in dishes_data:
    img_file = get_image_file(d['image_url'], d['filename'])
    item = MenuItem(
        category=d['category'],
        name=d['name'],
        description=d['description'],
        price=d['price'],
        spice_level=d.get('spice_level', 'none'),
        is_vegetarian=d.get('is_vegetarian', False),
        is_vegan=d.get('is_vegan', False),
        is_gluten_free=d.get('is_gluten_free', False),
        is_featured=d.get('is_featured', False),
        ingredients=d.get('ingredients', ''),
        prep_time=d.get('prep_time', 20),
        calories=d.get('calories', None),
        chef_notes=d.get('chef_notes', ''),
        order=d.get('order', 0),
    )
    if img_file:
        item.image.save(d['filename'], img_file, save=False)
    item.save()

print(f"Created {MenuItem.objects.count()} menu items.")

# 4. Create Gallery Images
gallery_data = [
    {
        'caption': 'Intimate Dining Room Ambiance',
        'category': 'ambiance',
        'url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1000&auto=format&fit=crop&q=80',
        'file': 'ambiance_1.jpg',
        'order': 1
    },
    {
        'caption': 'A5 Wagyu Preparation by Chef Marco',
        'category': 'chefs',
        'url': 'https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=1000&auto=format&fit=crop&q=80',
        'file': 'chef_1.jpg',
        'order': 2
    },
    {
        'caption': 'Private Sommelier Wine Cellar',
        'category': 'ambiance',
        'url': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1000&auto=format&fit=crop&q=80',
        'file': 'cellar_1.jpg',
        'order': 3
    },
    {
        'caption': 'Fresh Maine Lobster & Saffron Risotto',
        'category': 'food',
        'url': 'https://images.unsplash.com/photo-1559737197-69c86d681e13?w=1000&auto=format&fit=crop&q=80',
        'file': 'food_lobster.jpg',
        'order': 4
    },
    {
        'caption': 'Evening Terrace Lounge & Bar',
        'category': 'exterior',
        'url': 'https://images.unsplash.com/photo-1543007630-9710e4a00a20?w=1000&auto=format&fit=crop&q=80',
        'file': 'terrace_1.jpg',
        'order': 5
    },
    {
        'caption': 'Handcrafted Botanical Cocktails',
        'category': 'food',
        'url': 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=1000&auto=format&fit=crop&q=80',
        'file': 'cocktails_1.jpg',
        'order': 6
    },
]

for g in gallery_data:
    img_file = get_image_file(g['url'], g['file'])
    g_obj = GalleryImage(
        caption=g['caption'],
        category=g['category'],
        order=g['order']
    )
    if img_file:
        g_obj.image.save(g['file'], img_file, save=False)
    g_obj.save()

print(f"Created {GalleryImage.objects.count()} gallery images.")

# 5. Create Team Members
team_data = [
    {
        'name': 'Marco Delacroix',
        'role': 'Executive Chef & Founder',
        'specialty': 'French-Japanese Culinary Arts',
        'bio': 'Trained at Le Cordon Bleu Paris and 3-Michelin star kitchens in Tokyo. 22 years of passion crafting Savoir\'s signature style.',
        'url': 'https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=800&auto=format&fit=crop&q=80',
        'file': 'chef_marco.jpg',
        'order': 1
    },
    {
        'name': 'Isabelle Martin',
        'role': 'Head Pastry Chef',
        'specialty': 'Artisanal Patisserie & Chocolate',
        'bio': 'Former lead pastry artisan at Pierre Hermé Paris. Celebrated for ethereal soufflés and architectural chocolate sculptures.',
        'url': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80',
        'file': 'pastry_isabelle.jpg',
        'order': 2
    },
    {
        'name': 'Julien Mercier',
        'role': 'Master Sommelier',
        'specialty': 'Old & New World Vintage Pairings',
        'bio': 'Certified Master Sommelier with over two decades managing elite wine programs across Europe and New York.',
        'url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800&auto=format&fit=crop&q=80',
        'file': 'sommelier_julien.jpg',
        'order': 3
    },
]

for t in team_data:
    img_file = get_image_file(t['url'], t['file'])
    t_obj = TeamMember(
        name=t['name'],
        role=t['role'],
        specialty=t['specialty'],
        bio=t['bio'],
        order=t['order']
    )
    if img_file:
        t_obj.photo.save(t['file'], img_file, save=False)
    t_obj.save()

print(f"Created {TeamMember.objects.count()} team members.")

# 6. Create Testimonials
testimonials_data = [
    {
        'name': 'Evelyn Montgomery',
        'rating': 5,
        'review': 'Savoir provides one of the finest dining experiences in North America. The A5 Wagyu Tenderloin melted in my mouth, and the wine pairings were immaculate.',
        'source': 'The New York Gourmet Review'
    },
    {
        'name': 'Chef Jean-Pierre Laurent',
        'rating': 5,
        'review': 'Chef Marco\'s precision and balance of flavors is extraordinary. Every course of the tasting menu tells a compelling story.',
        'source': 'Michelin Guide Inspector'
    },
    {
        'name': 'Dr. Marcus Vance',
        'rating': 5,
        'review': 'We celebrated our 20th wedding anniversary here. From the personalized greeting to the surprise dessert arrangement, it was perfection.',
        'source': 'OpenTable Verified Guest'
    },
    {
        'name': 'Sophia & David Chen',
        'rating': 5,
        'review': 'The Périgord Black Truffle Pasta alone makes the trip to New York worthwhile. The atmosphere is warm, intimate, and impossibly chic.',
        'source': 'TripAdvisor Platinum Reviewer'
    },
]

for t in testimonials_data:
    Testimonial.objects.create(
        name=t['name'],
        rating=t['rating'],
        review=t['review'],
        source=t['source']
    )

print(f"Created {Testimonial.objects.count()} testimonials.")
print("Seeding completed successfully!")
