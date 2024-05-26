CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    token VARCHAR (255) NULL
);

CREATE TABLE information_categories (
    id SERIAL PRIMARY KEY,
    label VARCHAR(50) NOT NULL
);

CREATE TABLE information_lists (
    id SERIAL PRIMARY KEY,
    information_category_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    image TEXT NULL,
    timeRelevancy DATE NOT NULL,

    FOREIGN KEY (information_category_id) REFERENCES information_categories (id)
);

CREATE TABLE prompt_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    information_category_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(100) NOT NULL,
    probability INT NOT NULL,
    reason TEXT NOT NULL,

    FOREIGN KEY (information_category_id) REFERENCES information_categories (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE chat_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users (id)
);

GRANT ALL PRIVILEGES ON TABLE users TO lsffsezngtsopp;
GRANT ALL PRIVILEGES ON TABLE information_categories TO lsffsezngtsopp;
GRANT ALL PRIVILEGES ON TABLE information_lists TO lsffsezngtsopp;
GRANT ALL PRIVILEGES ON TABLE prompt_logs TO lsffsezngtsopp;
GRANT ALL PRIVILEGES ON TABLE chat_logs TO lsffsezngtsopp;

-- GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO lsffsezngtsopp;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO lsffsezngtsopp;

INSERT INTO users (username, password, is_admin) VALUES
('admin', 'scrypt:32768:8:1$t3QxtxoWuRvcYh2S$6a106cb9dfb6f3d602d09502d3eb8bcfe3d86e5406a7f048ad1a4be6edb69efb520c947e7ee7d8b249ea54fef603ca16ab23b8cafb21d0aa7d74cb7fdc70dfee', true);

INSERT INTO information_categories (label) VALUES
('Politics'),
('Economic'),
('Culture'),
('Film'),
('Congressional Memo');

INSERT INTO information_lists (information_category_id, title, content, image, timerelevancy) VALUES
(2, 'PAM Jaya Targets Fulfillment of 100 Percent Drinking Water Pipeline by 2030', '<p>The development of the Drinking Water Supply System (SPAM) in DKI Jakarta Province is an effort to achieve the service target of up to 100 percent of the citizens of the capital city by 2030. The DKI Jakarta Regional Owned Enterprise (BUMD), PAM Jaya, on Monday held a discussion virtual world with the theme of the SPAM development plan in Jakarta. PAM Jaya President Director Arief Nasrudin said piped drinking water services of course have a domino effect, starting from the environment and the health of Jakarta residents.</p>

<p>&quot;As we know, according to 2018 research data, around 45 percent of the Jakarta area has groundwater with critical quality to damage,&quot; said Arief. Arief added, providing access to piped drinking water can reduce the exploitation of groundwater which has an impact on environmental damage, health problems, and potential environmental disasters. 90 percent of the area in Jakarta, especially in the northern region, is predicted to sink by 2050 because the land level is getting lower.</p>

<p>&quot;In the near future, when this continues, in 2050 it is predicted that 90 percent of the Jakarta area, especially in the northern part, will be submerged due to culture or water use which is not immediately resolved,&quot; said Arief.</p>

<p>DKI Jakarta Development and Environment Assistant, Afan Adriansyah Idris said that his party had established a synergy by signing a memorandum of understanding between the Ministry of Home Affairs, Ministry of Public Works and Public Housing (PUPR) and PAM Jaya. The memorandum of understanding then underlies the Governor&#39;s Regulation Number 7/2022 regarding the assignment to PAM Jaya to accelerate the increase in the coverage of drinking water services in DKI Jakarta Province.</p>

<p>&quot;Service coverage has only reached around 64 percent, while the target for service coverage is 100 percent by 2030. Therefore, the SPAM development program in DKI Jakarta Province is urgently needed,&quot; Afan said.</p>

<p>PAM Jaya consultant Noviyan Halim explained that currently PAM Jaya requires an increase in service coverage to 36 percent and a water supply of 11,150 liters per second to achieve 100 percent service coverage. Noviyan added that the SPAM development project is a solution to meet these needs, namely through the Karian Serpong SPAM with a capacity of 3,200 liters per second (lpd) and the Ciliwung SPAM 200 lpd. Furthermore, SPAM Pesanggrahan 750 lpd, SPAM Jatiluhur I 4,000 lpd, SPAM Buaran 3 3,000 lpd and SPAM Ir H Djuanda/Jatiluhur II 2,054 lpd.&nbsp;</p>
', '2024-05-23_18-14-11_665382_b2ap3_large_pedagang-air-eceran-muara-angke--12-tirto.id-andrey-gromico_ratio-16x9_1.jpg', '2020-08-08'),
(4, 'Rebel Moon 2 sets unwanted record for Zack Snyder', '<p><em><a href="https://www.digitalspy.com/movies/a46164088/rebel-moon-2-release-date/" target="_blank">Rebel Moon &ndash; Part Two: The Scargiver</a></em>&nbsp;has set an unwanted record for director&nbsp;<a href="https://www.digitalspy.com/tv/ustv/a60285966/zack-snyder-until-the-last-one/" target="_blank">Zack Snyder</a>, marking the lowest&nbsp;<a href="https://www.rottentomatoes.com/celebrity/zack_snyder" target="_blank">Rotten Tomatoes</a>&nbsp;score of his career.</p>

<p>Following its release last week, the movie &ndash; which follows on from last year&#39;s&nbsp;<em>Part One: A Child of Fire</em>&nbsp;&ndash; already&nbsp;<a href="https://www.digitalspy.com/movies/a60547758/rebel-moon-2-rotten-tomatoes/" target="_blank">attained a brutal score on the site</a>.</p>

<p>Rotten Tomatoes has now confirmed that&nbsp;<em>The Scargiver</em>&nbsp;is the lowest-rated film for Snyder, sitting at&nbsp;<a href="https://www.rottentomatoes.com/m/rebel_moon_part_two_the_scargiver" target="_blank">15%</a>&nbsp;at the time of writing &ndash; a bit below the first movie&#39;s&nbsp;<a href="https://www.rottentomatoes.com/m/rebel_moon_part_1_a_child_of_fire" target="_blank">21%</a>&nbsp;score.</p>

<p><a href="https://www.digitalspy.com/movies/a60522104/rebel-moon-2-review-scargiver/" target="_blank"><strong>Digital Spy</strong>&nbsp;said</a>&nbsp;in our two-star review that the sequel &quot;suffers from the same flaws&quot; as the first movie and that it is &quot;hard to imagine anybody other than hardcore Snyder fans wanting to revisit this world&quot;.</p>

<p>&quot;There&#39;s no denying Snyder has created an interesting world &ndash; he just forgot to tell an interesting story within it,&quot; we added.</p>

<p><em><a href="https://collider.com/rebel-moon-part-two-the-scargiver-review/" target="_blank">Collider</a>&nbsp;</em>called the sequel &quot;even worse than&nbsp;<em>Part One</em>&quot; and that its &quot;ambitions have gotten infinitely smaller&quot;, while&nbsp;<em><a href="https://www.thewrap.com/rebel-moon-part-2-the-scargiver-review-zack-snyder-netflix/" target="_blank">TheWrap</a></em>&nbsp;labelled both movies &quot;shallow and generic space operas, distractingly derivative of better films while adding very little to the mix&quot;.</p>

<p>Last month, star Sofia Boutella&nbsp;<a href="https://www.digitalspy.com/movies/a60108203/rebel-moon-sofia-boutella-reviews/" target="_blank">opened up about the first movie&#39;s negative reviews</a>, telling&nbsp;<em><a href="https://www.vulture.com/article/sofia-boutella-action-movies-hollywood.html" target="_blank">Vulture</a></em>: &quot;I always thought that I was fully armed to take on those punches, and then I read the critics that came down on&nbsp;<em>Rebel Moon</em>,&nbsp;and it really affected me.</p>

<p>&quot;And I&#39;m just gonna be honest about it. I feel like I&#39;m carrying it for everybody that cared so much about this project, and that&#39;s what affected me. Not the way I look. If anything, I&#39;ve been pretty lucky and people like my work in it, but the movie was criticized.</p>

<p>&quot;It really affected me for all of those who put so much heart, tears, and sweat in this project. It&rsquo;s hard to see something being demolished to that extent.&quot;</p>

<p>Boutella added that she was &quot;proud to have been part of it&quot; and that&nbsp;<em>Rebel Moon</em>&nbsp;will be a &quot;very important part of my life that I will defend forever&quot;.</p>

<p><strong><em>Rebel Moon &ndash; Part One: A Child of Fire</em>&nbsp;and&nbsp;<em>Rebel Moon &ndash; Part Two: The Scargiver</em>&nbsp;are available to watch on Netflix.</strong></p>

<p>Source:&nbsp;<a href="https://www.digitalspy.com/movies/a60601178/rebel-moon-2-zack-snyder-unwanted-record/" target="_blank">https://www.digitalspy.com/movies/a60601178/rebel-moon-2-zack-snyder-unwanted-record/</a></p>
', '2024-05-23_18-26-33_634259_19c9575532d5bf053e56a9b2502065bf_1.jpg', '2024-04-25'),
(1, 'Israeli Troops Shoot Dead 2 Palestinian Men in West Bank', '<p>Jakarta - Pasukan Israel menembak mati dua pria Palestina di sebuah pos militer dekat kota Jenin di Tepi Barat pada hari Sabtu (27/4).</p>

<p>Dalam sebuah pernyataan, militer Israel menyatakan bahwa insiden itu terjadi ketika beberapa militan tiba dengan sebuah kendaraan dan menembaki para tentara yang ditempatkan di pos militer Salem di pintu masuk Jenin.</p>

<p>&quot;Para prajurit, yang telah ditempatkan sebelumnya karena beberapa insiden serupa di masa lalu, berhasil melenyapkan dua teroris,&quot; kata militer Israel, seperti dikutip kantor berita AFP, Sabtu (27/4/2024).</p>

<p>Kantor berita resmi Palestina, Wafa mengatakan pasukan Israel membunuh Mustafa Sultan Ahmed, 22, dan Ahmed Muhammad Shawahna, 21, di pos militerr tersebut. Disebutkan bahwa dua orang lainnya terluka dan dirawat di rumah sakit.</p>

<p>Wafa melaporkan bahwa pasukan Israel menahan jenazah mereka setelah menolak akses petugas medis ke jenazah mereka.</p>

<p>Pasukan Israel kerap melakukan penggerebekan di Jenin dan sekitarnya dan di kamp-kamp pengungsi di dekatnya, yang merupakan pusat kelompok-kelompok militan.</p>

<p>Tepi Barat, yang diduduki Israel sejak tahun 1967, telah mengalami peningkatan kekerasan selama lebih dari setahun, terutama sejak perang Israel-Hamas meletus pada tanggal 7 Oktober.</p>

<p>Setidaknya 490 warga Palestina telah dibunuh oleh pasukan Israel atau pemukim di Tepi Barat sejak 7 Oktober, menurut para pejabat Palestina.<br />
Jalur Gaza telah dilanda perang sejak kelompok Hamas dan militan Palestina lainnya melancarkan serangan yang belum pernah terjadi sebelumnya terhadap Israel selatan pada 7 Oktober.</p>

<p>Serangan itu mengakibatkan kematian 1.170 orang, termasuk warga Israel dan orang asing, menurut penghitungan AFP berdasarkan angka resmi Israel.</p>

<p>Serangan balasan Israel terhadap Jalur Gaza yang dikuasai Hamas, telah menewaskan sedikitnya 34.356 warga Palestina. Kebanyakan dari mereka adalah wanita dan anak-anak, menurut kementerian kesehatan wilayah tersebut.</p>

<p>Source:&nbsp;<a href="https://news.detik.com/internasional/d-7313509/pasukan-israel-tembak-mati-2-pria-palestina-di-tepi-barat/2" target="_blank">https://news.detik.com/internasional/d-7313509/pasukan-israel-tembak-mati-2-pria-palestina-di-tepi-barat/2</a></p>
', '2024-05-23_18-35-21_193525_2024-04-20T220748Z_1560470943_RC2HA7AT1887_RTRMADP_3_ISRAEL-PALESTINIANS-WEST-BANK-RAID-1713651935.jpg', '2024-04-27'),
(5, 'Schumer Says Foreign Aid Victory Shows Congress Isn’t Broken', '<p>Senator Chuck Schumer, the New York Democrat and majority leader, insists that Congress isn&rsquo;t broken &mdash; it just has a stubborn glitch.</p>

<p>As he celebrated approval this week of a major&nbsp;<a href="https://www.nytimes.com/2024/04/24/us/politics/biden-ukraine-israel-aid.html">national security spending measure</a>&nbsp;to aid Ukraine and Israel that took months of wrangling and strategizing, Mr. Schumer said the success of the package validated his view that bipartisanship can prevail once extreme elements on Capitol Hill are sidelined.</p>

<p>&ldquo;I don&rsquo;t think that Congress is dysfunctional,&rdquo; Mr. Schumer said in an interview. &ldquo;It&rsquo;s that there are some dysfunctional people in Congress, and we can&rsquo;t let them run the show.&rdquo;</p>

<p>The majority leader said that the passage of the foreign aid bill, the renewal of a&nbsp;<a href="https://www.nytimes.com/2024/04/20/us/politics/senate-passes-surveillance-law-extension.html">warrantless electronic surveillance program</a>&nbsp;and the approval of government funding for the year have shown that Congress can still function if its damaging glitch &mdash; right-wing lawmakers invested in chaos &mdash; is dealt out.</p>

<p>&ldquo;They are nasty, they are negative and they don&rsquo;t want to get anything done at all,&rdquo; Mr. Schumer said of far-right Republicans in the House. He noted that Congress had been able to move ahead on big issues once Speaker Mike Johnson and a significant bloc of House Republicans decided to marginalize the ultraconservatives, even though it has prompted a threat to Mr. Johnson&rsquo;s speakership.</p>

<p>&ldquo;The idea that Congress can&rsquo;t function in this modern world with technology and everything else &mdash; which admittedly makes it harder &mdash; has been disproved by a whole lot of things that succeeded in a bipartisan way,&rdquo; he said. &ldquo;But in each case, the hard right had to be resisted.&rdquo;</p>

<p>Since Republicans took control of the House in 2023, Mr. Schumer has repeatedly emphasized that any measures intended to become law would need to be shaped in a bipartisan way because the Senate and White House are under the control of Democrats.</p>

<p>It sounds like common sense, considering the partisan divide and the need for the House, Senate and President Biden to ultimately sign off. But it has not proven so easy to achieve given the attempts by the far right to exert its influence and insist on its positions.</p>

<p>The federal government over the past year came perilously close to a first-ever default and escaped damaging government shutdowns multiple times only at the very last minute. At the same time, House Republicans have tried to build a case to impeach Mr. Biden and did impeach his homeland security secretary, Alejandro N. Mayorkas, only to watch Senate Democrats dismiss the case in about three hours, setting off a string of Republican recriminations.</p>

<p>The foreign aid bill was also approved only after months of delay and after being declared all but dead. But the outcome has stirred discussion on Capitol Hill over whether a Congress that has struggled do much has finally found a governing center that could revive the legislative process.</p>

<p>Events will have to play out over the coming months to test that theory, but significant differences remain between the two parties that will make finding common ground difficult and&nbsp;<a href="https://www.nytimes.com/2024/03/08/us/politics/congress-dysfunction-spending-bills.html">the coalition governing that has broken out</a>&nbsp;<a href="https://www.nytimes.com/2024/03/08/us/politics/congress-dysfunction-spending-bills.html">on Capitol Hill</a>&nbsp;in recent months&nbsp;<a href="https://www.nytimes.com/2024/04/21/us/politics/house-aid-coalition-ukraine-israel.html">hard to replicate</a>. An approaching election will only highlight the divide.</p>

<p>Approving the foreign bill could make it more difficult to coalesce, as Republicans who backed it retrench to reassure their voters of their conservative bona fides in the run-up to the election. For instance, Mr. Johnson, under fire from the far right for bringing the Ukraine aid to the floor, traveled to New York on Wednesday to denounce the pro-Palestinian student protests at Columbia University. The visit drew him praise from some unhappy with his handling of the aid package, but exacerbated a bitter split among lawmakers over the Israel-Gaza war.</p>

<p>Even as Mr. Schumer joined forces with Senator Mitch McConnell of Kentucky, the Republican leader, on the aid to Ukraine, Mr. McConnell was hammering his Democratic counterpart for&nbsp;<a href="https://www.nytimes.com/2024/03/19/us/politics/schumer-israel-netanyahu-gaza.html">calling for a change in the Israeli government</a>&nbsp;once the conflict in Gaza was settled. Their Ukraine partnership reflected common cause on that topic, not a realignment on a host of issues. Mr. McConnell is now intensely focused on winning Senate seats and making Mr. Schumer the minority leader next year.</p>

<p>&ldquo;We did work together on this; we both thought it was important to do it,&rdquo; Mr. McConnell said of his partnership with Mr. Schumer on Ukraine. &ldquo;But it wasn&rsquo;t about relationships. It was about the substance.&rdquo;</p>

<p>The universe of existential issues that can cause lawmakers to rise to the occasion, such as the push to assist a democratic ally in a battle for survival against Russian aggression, is also limited. Immigration issues continue to divide the parties significantly, as evidenced by the collapse of a&nbsp;<a href="https://www.nytimes.com/2024/02/06/us/politics/border-republicans-ukraine-bill.html">bipartisan border security bill</a>&nbsp;in February. A bipartisan House-passed&nbsp;<a href="https://www.nytimes.com/2024/03/13/us/politics/tax-bill-child-credit-senate.html">tax bill</a>&nbsp;has stalled in the Senate despite widespread support, as Republicans assess whether they might get a better deal next year if they win the majority.</p>

<p>Fundamental institutional problems also exist that could inhibit a new turn toward bipartisanship. At a seminar on &ldquo;Fixing Congress&rdquo; convened on Thursday by the University of Pennsylvania&rsquo;s Penn Biden Center on Capitol Hill, former senators and House members dissected a number of developments hindering Congress.</p>

<p>The list included a very short workweek, siloing by party, reluctance to take tough votes, decreasing emphasis on policy expertise, a preponderance of leader-driven legislation and the always intense focus on primary challenges and re-election.</p>

<p>&ldquo;There really isn&rsquo;t a governing mentality in Washington right now,&rdquo; said John Yarmuth, a former Democratic House member from Kentucky who led the Budget Committee. &ldquo;There is an electoral mentality.&rdquo;</p>

<p>But Mr. Schumer says he sees cause for hope. He noted that Democrats were secure enough in their political standing that they were willing to make serious concessions on border security to strike a deal with Senate Republican negotiators even though it fell apart once it came under attack from former President Donald J. Trump.</p>

<p>&ldquo;I&rsquo;m an optimist,&rdquo; Mr. Schumer said. &ldquo;You&rsquo;ve got to persist, you&rsquo;ve got to be bipartisan and you&rsquo;ve got to resist the clarion call of MAGA.&rdquo;</p>

<p>Source:&nbsp;<a href="https://www.nytimes.com/2024/04/26/us/politics/schumer-israel-ukraine-aid-congress.html" target="_blank">https://www.nytimes.com/2024/04/26/us/politics/schumer-israel-ukraine-aid-congress.html</a></p>
', '2024-05-23_18-37-44_689277_Schumer-1702409397.jpg', '2024-04-26'),
(2, '''When will our good days come?'' The Mumbai cook strapped for cash', '<p><em><strong>What&#39;s your money worth? A&nbsp;<a href=\""https://www.aljazeera.com/tag/whats-your-money-worth/\"">series</a>&nbsp;from the front lines of the cost-of-living crisis, where people who have been hit hard share their monthly expenses.</strong></em></p>

<p><strong>Name:</strong>&nbsp;Manisha Santosh Kadam</p>

<p><strong>Age:</strong>&nbsp;42</p>

<p><strong>Born:</strong>&nbsp;Manchar, in the Indian state of Maharashtra</p>

<p><strong>Occupation:</strong>&nbsp;Cook</p>

<p><strong>Lives with:</strong>&nbsp;Her husband, Santosh, 48, their daughter, Rithuja, 21, and son, Sujal, 17.</p>

<p><strong>Lives in:</strong>&nbsp;A 37sq-metre (400sq-foot) house in Diva, located in Maharashtra&#39;s Thane district, which is about an hour&#39;s drive from Mumbai, India&rsquo;s financial capital.</p>

<p>The house, which is located on a busy street, has two small rooms - a medium-sized hall where all of them sleep together, and a kitchen. They do not have a garden or any open space.</p>

<p><strong>Monthly income:</strong>&nbsp;Working as a cook for eight hours a day at a household in the Byculla area of South Mumbai, Manisha earns a wage of 17,000 rupees ($203.64) per month. India&#39;s daily minimum wage is currently 176 rupees ($2.11).</p>

<p>Manisha&#39;s husband works as an electrician and earns an erratic income ranging from 3,000 to 4,000 rupees a month ($35.94 to $47.92).</p>

<p><strong>Total expenses for the month:</strong>&nbsp;16,673 rupees ($199.72) on family living expenses. At the end of March, Manisha only had 327 rupees ($3.92) left in her bank account.</p>

<p>She also paid 90,000 rupees ($1,078) to repay a loan she had taken from the government to cover running costs at their family farm near the town of Manchar, where Manisha is from. She paid back the loan by borrowing money from friends and relatives.</p>

<p>Every morning, in the hours before dawn, more than six million people board suburban railway trains in Mumbai to travel for work or study.</p>

<p>Manisha Santosh Kadam, 42, is among them - on her one-hour, 20-minute commute from her home in Diva, on the outskirts of Mumbai to the upmarket suburb of Byculla, where she has worked as a cook in a household for the past two years.</p>

<p>Manisha wakes up just before sunrise, completes her chores and rushes to work.</p>

<p>She came to Mumbai from her village near Manchar, which is about three and a half hours away from the big city, 12 years ago with high hopes. Manisha and her husband are Marathas - a group of castes comprising farmers, warriors and some landowners.</p>

<p>&quot;Like many who come to this bustling city to fulfil their dreams, I also came here from my village 12 years ago, with the hope that Mumbai will be a nice place to work, earn a livelihood and send my children to school,&quot; she says as she looks out of the train window at the passing urban cityscape.</p>

<p>Manisha, who is one of four siblings, has been earning money for her family since she was just 10 years old. Alongside her studies until the tenth grade and then after she stopped going to school, she spent her late childhood and teenage years working on her family&rsquo;s vegetable farm in Manchar.</p>

<p>She was still farming after she got married and had children but she earned just 25 rupees ($0.30) each day of the season, which lasted from the onset of the monsoon in June until the Diwali festival of November, cultivating rice, potato and millets. Twelve years ago, her husband, an electrician, was unemployed and the family found itself struggling to make ends meet on the little Manisha was earning. So, they decided to move to Mumbai.</p>

<p>&quot;My daughter was in the third grade and my son was just an infant when we came to Mumbai,&rdquo; says Manisha. &ldquo;Life is very fast-paced here,&quot; she adds as she prepares to get off the train, which is pulling into Dadar station, a busy interchange station for the suburban trains of Mumbai.</p>

<p>Manisha rushes through the crowds of people to catch her next train towards Byculla station, which is close to her workplace in south Mumbai. Nobody seems to pause for breath at this station. Everyone is impatient and determined to get to their destinations as quickly as possible.</p>

<p>&quot;This is what the fast life of Mumbai looks like in my daily commute, where I pay 215 rupees ($2.58) for a monthly ticket. This is the peak time to travel since everyone is going to their workplace,&rdquo; Manisha says. &ldquo;While there is no space to sit in the train, it also feels like there is no space to breathe.</p>

<p>&quot;But before this job, life seemed like an uphill battle.&quot;</p>

<h2>&#39;Education is more valuable than a couple of jewels&#39;</h2>

<p>When Manisha came to Mumbai in 2011, India, like other emerging economies, was also wading through the effects of the euro debt crisis, which had triggered a global economic slowdown. The Indian rupee was weak at about 50 to the dollar (it has since worsened to 83.52 against the dollar this week) and unemployment, an issue which continues to challenge the country, was widely prevalent.</p>

<p>Manisha and her family were also instantly affected by the economic slowdown. While she was trying to find a well-paid job in Mumbai, Manisha began selling vegetables in the Diva neighbourhood of the city, where she and her family were living in their small house which she had bought by selling all her jewels and other valuables.</p>

<p>&quot;I wanted the children to be comfortable and start going to school. Education is more valuable than a couple of jewels,&quot; she says.</p>

<p>But selling vegetables barely scratched the surface of her family&rsquo;s expenses and her dream of sending her children to school had to be temporarily put on the back burner. The childcare costs for her son would have been unaffordable if her daughter had also gone to school rather than staying at home to watch him while her mother was at work.</p>

<p>&quot;I would wake up early, rush to Mumbai&#39;s Kalyan neighbourhood, buy vegetables and then resell them in Diva. I would only earn about 100 rupees per day ($1.20) as profit through this job,&quot; she says.</p>

<p>&quot;My daughter couldn&#39;t go to school for a month because we couldn&#39;t afford it and she didn&#39;t want to leave her baby brother alone. I don&#39;t know how we went about life then. I feel like crying when I think about it.&quot;</p>

<p>Eventually, Manisha found a job at a women&rsquo;s clothing store, where she was hired as a seamstress. The shop wasn&#39;t far away from her house and also gave her the flexibility to take care of her children at home without additional childcare costs for her son.</p>

<p>&quot;I would earn between 3,000 to 4,000 rupees ($35.94 to $47.92) a month and this money helped me pay my daughter&#39;s school fees,&quot; she said.</p>

<p>While her husband had also secured a job as an electrician during this period, Manisha says he used his earnings primarily for his own needs - which included visiting their family village to check on the farm - only occasionally buying food for the children.</p>

<p>&quot;In many families in our community, it is the women who are the responsible family members and tend to run the household. While I love my husband and we live together, I have given up telling him about the importance of helping the family,&quot; she says.</p>

<h2>Demonetisation and a pandemic</h2>

<p>In 2016, India&#39;s Prime Minister Narendra Modi introduced a concept called &quot;demonetisation&quot;, seeking to tackle&nbsp;<a href=\""https://www.pmindia.gov.in/en/news_updates/tough-line-on-black-money-full-text-of-pm-modis-interview-to-network18/\"">black money</a>&nbsp;or unaccounted income in the country. Under this scheme, Modi said that the 500-rupee ($5.99) and 1,000-rupee ($11.98) currency notes would no longer be considered legal tender.</p>

<p>Manisha recollects watching the prime minister&#39;s speech on a television screen near the garment store and describes how people instantly rushed to banks to exchange the banned high-value notes.</p>

<p>Within days, the clothing store was forced to close because the business operated primarily through cash transactions and demonetisation had made many such transactions impossible. Manisha found herself unemployed, once again.</p>

<p>&quot;Once again the poor had to bear the brunt of a government policy. We never benefitted from demonetisation. It just made life even harder,&quot; she says.</p>

<p>But within a year, with her sister-in-law&#39;s help, Manisha got a job as a cook, at an office in south Mumbai&#39;s Marine Lines locality - an area known for the city&#39;s famous Wankhede Stadium, which hosts international cricket matches.</p>

<p>&quot;This was my first big job which paid me 15,000 rupees ($179.68) every month. The day I got this salary for the first time, I was thrilled and went to buy ladoos (a type of Indian sweet) for my family,&quot; Manisha says.</p>

<p>But three years later, with the onset of the coronavirus pandemic, her workplace downsized the firm and Manisha was unemployed again and the family moved back to their village to shelter from the pandemic.</p>

<p>&quot;I worked on the farm to earn some money. We also managed to make ends meet by depending on about 15,000 rupees ($179.68) I had saved through my previous job. But we returned to Mumbai after 10 months because for how long could we live off our savings?&quot;</p>

<p>After a brief stint as a cook in another office in Marine Lines - where Manisha also lived in order to not defy lockdown rules - she finally secured her current job in south Mumbai.</p>

<p>&quot;I&#39;ve been working in this household for two years and earn 17,000 rupees ($200) a month. I enjoy it and finally feel at peace,&quot; she said.</p>

<h2>&#39;When will our good days come?&#39;</h2>

<p>Historically, the Marathas - the caste to which Manisha belongs - have been a dominant community in the state of Maharashtra, where Mumbai and Manisha&rsquo;s village are. Shivaji - the founder of the empire - is widely revered across Maharashtra.</p>

<p>But Manisha feels that the government hasn&#39;t really helped their community - nor other poorer communities in the country.</p>

<p>She shows some government cards she has, ranging from a ration card - which allows her to buy groceries at a subsidised rate - to an Ayushman card (health insurance card), which she says are helpful. But it&rsquo;s not enough for people like her.</p>

<p>&quot;Throughout the pandemic and economic downfalls, all the political leaders kept promising aid packages to help us. But their national economic policies remain catered to aid the rich,&quot; she says.</p>

<p>&quot;Now as the elections are around the corner, we&#39;re hearing big money pledges once again and announcements saying &#39;acche din aayenge&#39; [a slogan used by Modi&#39;s party during elections which says good days are coming],&quot; Manisha said.</p>

<p>&quot;But when will our &#39;acche din&#39; [good days] come?&quot;</p>

<p>India heads to the polls in an election which will be held in seven stages between April 19 and June 4. It is the largest democratic exercise in the world. The constituencies across Mumbai, including Thane where Manisha lives, will go to the polls on May 20 in the fifth phase of India&#39;s mammoth seven-stage election which began this week.</p>

<p>Rahul Gandhi, the leader of the opposition Indian National Congress (INC) political party and Prime Minister Modi, the leader of the Bharatiya Janata Party (BJP), have begun their electoral campaigns by promising better infrastructure and more jobs for women and the poor, among other pledges.</p>

<p>Listening to some of the pledges on a radio while cooking at her workplace, however, Manisha isn&#39;t convinced.</p>

<p>&quot;When all the money they promise reaches our bank accounts - that time I will believe them,&quot; she said.</p>

<p>&quot;Politicians take from one hand but eat from two hands,&quot; Manisha adds.</p>

<p>&quot;I will vote in the elections but I don&#39;t expect politics to help my situation. In the end it will be the city of Mumbai which will help me reach my dreams.&quot;</p>

<p>Manisha&rsquo;s greatest dream is to ensure both her children are educated and can live a comfortable life. But with the cost of living rising, luxuries are impossible.</p>

<p>&quot;A few days back, my daughter asked for 100 rupees ($1.20) so that she could enjoy trying out a motorboat at the Juhu beach in Mumbai. But even to give her this small amount of money, I have to think twice,&quot; she says.</p>

<p>&ldquo;For now, we are able to make ends meet and after everything I&#39;ve experienced when it comes to money, I have learned not to spend unnecessarily. The rest is in God&#39;s hands,&quot; she said.</p>

<p>Source:&nbsp;<a href=\""https://www.aljazeera.com/economy/longform/2024/4/20/when-will-our-good-days-come-the-mumbai-cook-voting-in-indias-elections\"" target=\""_blank\"">https://www.aljazeera.com/economy/longform/2024/4/20/when-will-our-good-days-come-the-mumbai-cook-voting-in-indias-elections</a></p>
', '2024-05-23_18-40-48_922467_AP21273460434387-1696154581.jpg', '2024-04-20');