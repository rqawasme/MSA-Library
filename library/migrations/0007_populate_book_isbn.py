from django.db import migrations

# ISBN data sourced from library_20260328_034042.csv
# Keyed by exact title; matched case-insensitively at runtime.
BOOK_ISBN_MAP = {
    "Al-Shama'il Al-Muhammadiyya": "998438057",
    "How to Give Good Advice: The Difference Between Counsel & Shaming": "1966329334",
    "All the Sultan's Men": "1952306078",
    "Faris and the Curious Case of the Missing Eid Presents [Paperback] Muhammad Sattaur and Husna Sattaur [Paperback] Muhammad Sattaur and Husna Sattaur": "1952306132",
    "Who Is the Prophet Muhammad?": "1952306094",
    "O Son!": "1952306140",
    "The Book of Intentions: Towards a Life of Purpose & Clarity": "1952306612",
    "The Divine Reports: An English Translation of Mishkat al-Anwar": "1966329830",
    "Towards a True Spiritual Connection: Wisdom from the Teachings of Habib \u2018Umar bin Hafiz": "1952306671",
    "Slavery and Islam": "1786076357",
    "The Politics of Vulnerability: How to Heal Muslim-Christian Relations in a Post-Christian America: Today\u2019s Threat to Religion and Religious Freedom": "1643136623",
    "The Road to Mecca": "1887752374",
    "The Muqaddimah: An Introduction to History": "691166285",
    "The Tao of War": "1966329873",
    "Genghis Khan and the Making of the Modern World": "609809644",
    "Heart Therapy": "9675699531",
    "The Art of Learning: Timeless Wisdom for the Seeker of Knowledge": "1966329008",
    "Toward Sacred Activism": "1732258813",
    "Do not Be Envious (Golden Series Book-7)": "9960996700",
    "Some Secrets of the Divine Approach": "9811893942",
    "Islam and the Problems of the Youth": "9811860165",
    "To Every Young Woman Who Believes In Allah": "9811849072",
    "A Unique Pedagogical Approach in the Quran": "9811836604",
    "Inward Sin: The Greatest Danger in the Lives of Muslims": "9811828776",
    "Man and Allah\u2019s Justice on Earth": "9811814236",
    "The Content of Character": "985565934",
    "Supplement for the Seeker of Certitude: Worship from Zad al-Mustaqni`": "1944904093",
    "A Commentary upon the Creed of Imam al-Dardir": "9079294403",
    "The Alchemy of Happiness": "1684221668",
    "Apostate": "9079294322",
    "Kalam Cosmological Arguments": "1098544021",
    "Imam Abu Hanifa's Al-Fiqh Al-Akbar Explained": "1933764031",
    "Dedicating Rewards to the Deceased:: Reciting the Quran & Other Good Deeds": "9811870357",
    "Fiqh of Social Media": "1087931835",
    "The Rights of the Husband and Wife": "9811856729",
    "Outlines of Islamic Jurisprudence": "1541155327",
    "Islamic Legal Maxims: Qawa`id Fiqhiyyah": "1541147480",
    "Al-Fiqh Al-Manhaji, A Systematic Manual According to the Madhhab of Imam Ash-Shafi\u2019i: Purification and Prayer": "9811870896",
    "The Creed Made Easy al-\u2018Aqida al-Muyassira A bilingual introduction to Islamic theology Arabic - English": "9079294330",
    "Notions That Must Be Corrected": "907929425X",
    "Agenda to Change Our Condition": "985565918",
    "Purification of the Heart": "098556590X",
    "Being Muslim": "985565926",
    "The Scholars of the Sufis: They are the Genuine Followers of the Salaf": "9079294160",
    "A Critique of the Palmyran Creed: Deconstructing Ibn Taymiyya\u2019s Theology of Resemblance": "9079294268",
    "The Clear Quran": "097730096X",
    "Brand Islam": "1477309462",
    "Reconstruction of Religious Thought in Islam": "1541242173",
    "The Eternal Challenge": "1910952001",
    "El Cor\u00e1n - Esclarecedor | Paperback Paperback \u2013 January 1, 2020": "999721526",
    "Al-\u2018Arabiyya: Journal of the American Association of Teachers of Arabic, Volume 50": "1626165165",
    "Arabic Through the Qur\u2019an": "946621683",
    "Tafsir al-Qurtubi - Introduction: The General Judgments of the Qur\u2019an and Clarification of what it contains of the Sunnah and \u0100yahs of Discrimination": "1908892579",
    "Tafsir al-Qurtubi Vol. 2: Juz\u2019 2: S\u016brat al-Baqarah 142 - 253": "1908892757",
    "Tafsir al-Qurtubi Vol. 3: Juz\u2019 3: S\u016brat al-Baqarah 254 - 286 & S\u016brah \u0100li \u2018Imr\u0101n 1 - 95": "190889279X",
    "Muhammad: A Very Short Introduction": "199559287",
    "Misquoting Muhammad: The Challenge and Choices of Interpreting the Prophet\u2019s Legacy": "1780747829",
    "The Eternal Message of Muhammad": "946621489",
    "When The Moon Split": "9960897281",
    "Muhammad Pb": "42970504",
    "The Leadership of Muhammad": "749460768",
    "Hadith Nomenclature Primers": "985884061",
    "Hadith: Muhammad\u2019s Legacy in the Medieval and Modern World": "1786073072",
    "Riyad as-Salihin: The Meadows of The Righteous - Abridged And Annotated": "1906949476",
    "Al-Wafi: A Thorough Commentary on The Forty Nawawiyyah": "9811488460",
    "Muhammad the Perfect Man": "1909460001",
    "Al-Ghazali on the Condemnation of Pride and Self-admiration: Kitab dhamm al-kibr wa\u2019l-ujb": "1911141139",
    "Tafsir al-Qurtubi - Vol. 1: Juz\u2019 1: Al-F\u0101ti\u1e25ah & S\u016brat al-Baqarah 1-141": "1908892609",
    "Handbook of A Healthy Muslim Marriage: Unlocking The Secrets To Ultimate Bliss": "1933764163",
    "Al-Ghazali on Disciplining the Soul and on Breaking the Two Desires": "946621438",
    "The Virtues of Seclusion in Times of Confusion": "1944820930",
    "The Book of Assistance": "1887752587",
    "The Book of Wisdoms": "1933764058",
    "Al-Ghazali on the Remembrance of Death & the Afterlife": "1911141015",
    "Imam Al-Ghazali on Self-Delusion": "1915265428",
    "The Principles of the Creed: Book 2 of the Revival of the Religious Sciences": "1941610161",
    "The Mysteries of Purification: Book 3 of the Revival of the Religious Sciences": "1941610315",
    "The Book of Knowledge: Book 1 of The Revival of the Religious Sciences": "1941610153",
    "Food Between Curse and Cure: Islam, Health, and the Good Life": "578549840",
    "Man and the Universe": "9957230220",
    "Ascent to Felicity": "1933764090",
    "Hearts Turn: Sinners, Seekers, Saints and the Road to Redemption": "989364003",
    "Prayers for Forgiveness": "972835814",
    "A Concise Description of Jannah & Jahannam": "1842001205",
    "The Lives of Man: A Guide to the Human States: Before Life, In the World, and After Death": "1887752145",
    "On Remembering Death": "1905837615",
    "The Essential Islamic Creed": "993475604",
    "The Value of Time": "954329457",
    "Imam Al-Tahawi\u2019s Creed of Islam": "993475663",
    "THE ISLAMIC DISCOURSE IN RELIGIOUS INSTITUTIONS: IT\u2019S CURRENT STATE & FUTURE DEVELOPMENT": "1735376701",
    "World of the Angels": "1870582144",
    "Interpretation of Dreams": "187058208X",
    "The Differences of the Im\u0101ms": "1933764082",
    "The Mysteries of the Prayer and Its Important Elements": "1941610358",
    "A Handbook of Accepted Prayers": "1838049231",
    "A Handbook of Prophetic Characteristics": "1916824129",
    "A Handbook of Spiritual Medicine": "1838049207",
    "Khasa\u2019 ail Commentary of Shamail": "1906949743",
    "Daily Wisdom": "1847740324",
    "Fortress Of The Muslim (Du\u2019a From The Qur\u2019an & Sunnah)": "1910015172",
    "Understanding Islam and the Muslims: The Muslim Family and Islam and World Peace": "1887752471",
    "Islam": "1929694083",
    "Absolute Essentials of Islam": "972835849",
    "al-Khasa\u2019is al-Muhammadiyyah": "1952306450",
    "The Book on the Mysteries of the Pilgrimage for Young People": "1941610501",
    "Muhammad - The Last Prophet: A Model for All Time: A Model For All Time": "8119946103",
    'Miracles of the Prophet Muhammad: Selections from "The Shifa" of Qadi \'Iyad': "1952306175",
    "Muhammad: Prophet of Peace Amid the Clash of Empires": "156858783X",
    "Meeting Muhammad": "1847741770",
    "Celebrating the Birth of the Prophet": "195230606X",
    "Prayers Upon the Beloved: Supplications by Allah\u2019s Most Beautiful Names for the One Who Had the Most Beautiful Traits": "1952306043",
    "Khadijah": "1905516681",
    "Joy Jots": "999299042",
    "Prophetic Grace : The Qur\u2019anic Merits of the Prophet Muhammad": "990002608",
    "A Treasury of Hadith": "1847740677",
    "The Life of the Prophet Muhammad": "946621020",
    "The Prayer of the Oppressed w/ CD": "1450706088",
    "Muhammad: A Quranic Exposition of His Excellence and Virtues": "993475698",
    "The Subtle Blessings in the Saintly Lives of Abul-Abbas al- Mursi: And His Master Abul-Hasan": "1887752617",
    "Daily Wisdom: Sayings of the Prophet Muhammad": "1847740189",
}


def populate_isbn(apps, schema_editor):
    Book = apps.get_model('library', 'Book')
    # Build a lowercased lookup for case-insensitive matching
    lower_map = {title.lower(): isbn for title, isbn in BOOK_ISBN_MAP.items()}
    updated = 0
    for book in Book.objects.filter(isbn=''):
        isbn = lower_map.get(book.title.lower())
        if isbn:
            book.isbn = isbn
            book.save(update_fields=['isbn'])
            updated += 1


def reverse_isbn(apps, schema_editor):
    Book = apps.get_model('library', 'Book')
    known_isbns = set(BOOK_ISBN_MAP.values())
    Book.objects.filter(isbn__in=known_isbns).update(isbn='')


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_book_isbn'),
    ]

    operations = [
        migrations.RunPython(populate_isbn, reverse_isbn),
    ]
