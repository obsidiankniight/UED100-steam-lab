/*
 * UED100 Assessment 2 — Steam-inspired store redesign.
 * No external libraries, accounts, tracking, APIs or payments.
 * Data is fictional. User-controlled wishlist/cart/preferences live in browser localStorage.
 * All user-supplied titles enter the UI via textContent (not raw HTML).
 */
(() => {
  'use strict';
  const GAMES = window.STORE_GAMES || [];
  const PAGE = document.body.dataset.page || 'home';
  const $ = (sel, root=document) => root.querySelector(sel);
  const $$ = (sel, root=document) => [...root.querySelectorAll(sel)];
  const icon = (name, extra='') => `<svg class="ico ${extra}" aria-hidden="true"><use href="assets/icons/sprite.svg#${name}"></use></svg>`;
  const art = (game) => `assets/covers/${game.id}.svg`;
  const byId = id => GAMES.find(game => game.id === id);
  const money = value => new Intl.NumberFormat('en-AU', {style:'currency',currency:'AUD'}).format(value);
  const htmlSafe = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const readStore = (key, fallback) => { try { return JSON.parse(localStorage.getItem('ued100_'+key)) ?? fallback; } catch { return fallback; } };
  const writeStore = (key, value) => { try { localStorage.setItem('ued100_'+key,JSON.stringify(value)); } catch { /* Private modes may block persistence. UI still works. */ } };
  const initialSet = name => new Set(readStore(name,[]).filter(x => Boolean(byId(x))));
  const state = {
    wishlist:initialSet('wishlist'),cart:initialSet('cart'),
    hiddenShelves:new Set(readStore('hiddenShelves',[])),collapsed:new Set(readStore('collapsed',[])),
    nonsteam:readStore('nonsteam',[]).filter(x => typeof x==='string').slice(0,20)
  };
  let browse = {query:new URLSearchParams(location.search).get('q')||'', genre:new URLSearchParams(location.search).get('genre')||'All', sort:'popular'};
  const genres = ['All','Action','Adventure','RPG','Strategy','Simulation','Racing','Puzzle'];
  const getDiscount = g => g.oldPrice ? Math.round((1-g.price/g.oldPrice)*100) : 0;
  function toast(message){
    const stack=$('#toasts'); if(!stack)return;
    const item=document.createElement('div');item.className='toast';item.setAttribute('role','status');item.textContent=message;
    stack.appendChild(item);setTimeout(()=>item.remove(),3200);
  }
  function saveCollections(){writeStore('wishlist',[...state.wishlist]);writeStore('cart',[...state.cart]);updateCounts();}
  function updateCounts(){
    $$('.wishlist-count').forEach(n=>n.textContent=state.wishlist.size);
    $$('.cart-count').forEach(n=>n.textContent=state.cart.size);
    $$('.wishlist-counter').forEach(n=>n.textContent=state.wishlist.size?`(${state.wishlist.size})`:'');
    $$('.cart-counter').forEach(n=>n.textContent=state.cart.size?`(${state.cart.size})`:'');
    $$('.wishlist-navigation').forEach(n=>{n.setAttribute('aria-label',`Wishlist, ${state.wishlist.size} games`);n.classList.toggle('has-items',state.wishlist.size>0);});
    $$('.cart-navigation').forEach(n=>n.setAttribute('aria-label',`Shopping cart, ${state.cart.size} games`));
  }
  function wishlistButton(g, text=false){
    const yes=state.wishlist.has(g.id);
    return `<button type="button" class="${text?'btn btn-outline':''}${!text&&yes?' selected':''}" data-action="wishlist" data-id="${g.id}" aria-pressed="${yes}" aria-label="${yes?'Remove '+htmlSafe(g.title)+' from':'Add '+htmlSafe(g.title)+' to'} wishlist">${icon('heart')}${text ? (yes?'In wishlist':'Add to wishlist'):''}</button>`;
  }
  function cartButton(g, text=false){
    const yes=state.cart.has(g.id);
    return `<button type="button" class="${text?'btn btn-primary':''}${!text&&yes?' selected':''}" data-action="cart" data-id="${g.id}" aria-pressed="${yes}" aria-label="${yes?'Remove '+htmlSafe(g.title)+' from':'Add '+htmlSafe(g.title)+' to'} cart">${icon(yes?'check':'cart')}${text ? (yes?'In cart':'Add to cart'):''}</button>`;
  }
  function gameCard(g){
    return `<article class="game-card"><a class="game-art" href="game.html?id=${g.id}" aria-label="View details for ${htmlSafe(g.title)}"><img src="${art(g)}" alt="Illustrated artwork for ${htmlSafe(g.title)}" loading="lazy" width="1200" height="750"><span class="card-tag">${htmlSafe(g.badge)}</span></a><div class="game-copy"><a class="game-title" href="game.html?id=${g.id}">${htmlSafe(g.title)}</a><div class="game-meta">${htmlSafe(g.genre)} · ${g.rating}% positive reviews (demo)</div><div class="game-bottom"><div class="price-group">${g.oldPrice?`<span class="discount">-${getDiscount(g)}%</span><span class="old-price">${money(g.oldPrice)}</span>`:''}<span class="price">${money(g.price)}</span></div><div class="small-actions">${wishlistButton(g)}${cartButton(g)}</div></div></div></article>`;
  }
  function sectionHeader(title, desc, href, link){return `<div class="section-header"><div><h2>${title}</h2>${desc?`<p>${desc}</p>`:''}</div>${href?`<a href="${href}" class="text-link">${link||'View all'} ${icon('arrow-up-right')}</a>`:''}</div>`;}
  function gameShelf(id,title,desc,items){
    if(state.hiddenShelves.has(id))return '';
    const collapsed=state.collapsed.has(id);
    return `<section class="shelf ${collapsed?'collapsed':''}" id="shelf-${id}" aria-labelledby="shelf-title-${id}"><div class="section-header"><div><h2 id="shelf-title-${id}">${title}</h2><p>${desc}</p></div><button type="button" class="shelf-toggle" data-action="collapse" data-id="${id}" aria-expanded="${!collapsed}" aria-label="${collapsed?'Expand':'Collapse'} ${title}">${icon('chevron-down')}</button></div><div class="game-grid">${items.map(gameCard).join('')}</div></section>`;
  }
  function renderHome(){
    $('#main').innerHTML=`<section class="hero" aria-labelledby="hero-heading"><img class="hero-art" src="assets/covers/neon-drift.svg" alt="Original neon city racing artwork" width="1200" height="750"><div class="hero-copy"><div class="kicker">YOUR NEXT GREAT ESCAPE</div><h1 id="hero-heading">PLAY <span>BEYOND</span> THE ORDINARY.</h1><p>Discover something incredible. Less clutter, smarter choices, and all your favourite games in one place.</p><div class="hero-pills"><span class="pill">${icon('sparkles')} Curated for discovery</span><span class="pill">Featured: Neon Drift</span></div><div class="hero-actions"><a class="btn btn-primary" href="game.html?id=neon-drift">Explore featured game ${icon('arrow-right')}</a><a href="browse.html" class="btn btn-outline">Browse all games</a></div></div></section>
    <div class="feature-strip"><div class="feature"><span class="feature-icon">${icon('search')}</span><div><strong>Find it faster</strong><small>Search, filter and browse clearly</small></div></div><div class="feature"><span class="feature-icon">${icon('heart')}</span><div><strong>Your store, your way</strong><small>Personalise the shelves you see</small></div></div><div class="feature"><span class="feature-icon">${icon('shield')}</span><div><strong>Clear, safe interactions</strong><small>Accessible feedback and demo checkout</small></div></div></div>
    <section aria-labelledby="category-heading">${sectionHeader('What are you in the mood for?','A simpler path to the games you love',null)}<div class="category-row" id="category-heading">${genres.filter(x=>x!=='All').map(x=>`<a href="browse.html?genre=${encodeURIComponent(x)}" class="category-chip">${x}</a>`).join('')}</div></section>
    <div class="section-header" style="margin-top:42px"><div><h2>Made for your discovery</h2><p>Expand, collapse or hide sections — your layout preferences are saved locally.</p></div><button type="button" class="btn btn-outline" data-action="customize">${icon('settings')} Customise shelves</button></div>
    ${gameShelf('recommended','Curated for you','Explore these handpicked adventures.',[GAMES[0],GAMES[1],GAMES[3],GAMES[4]])}
    ${gameShelf('offers','Limited-time offers','Good games, better prices.',GAMES.filter(g=>g.oldPrice).slice(0,4))}
    ${gameShelf('popular','Popular right now','Highly rated games worth discovering.',[GAMES[6],GAMES[8],GAMES[9],GAMES[2]])}
    ${[...state.hiddenShelves].length?`<div class="notice" style="margin-top:26px">Some shelves are hidden. Use “Customise shelves” to bring them back.</div>`:''}
    <aside class="highlight"><div><div class="kicker">A FOCUS ON BETTER UX</div><h3>Your store should work for you.</h3><p>This student redesign simplifies discovery for new visitors while keeping wishlists, recommendations and game visibility useful for returning players and publishers.</p></div><a class="btn btn-primary" href="browse.html">Start exploring ${icon('arrow-right')}</a></aside>`;
  }
  function filterGames(){
    let results=GAMES.filter(g=>(browse.genre==='All'||g.genre===browse.genre));
    const q=browse.query.trim().toLowerCase();
    if(q)results=results.filter(g=>[g.title,g.genre,g.studio,...g.tags].some(t=>t.toLowerCase().includes(q)));
    if(browse.sort==='price-low')results.sort((a,b)=>a.price-b.price);
    if(browse.sort==='price-high')results.sort((a,b)=>b.price-a.price);
    if(browse.sort==='rated')results.sort((a,b)=>b.rating-a.rating);
    return results;
  }
  function updateBrowseResults(){
    const results=filterGames();
    const count=$('#result-count');if(count)count.textContent=`${results.length} game${results.length===1?'':'s'} found`;
    const target=$('#browse-results');if(!target)return;
    target.innerHTML=results.length?`<div class="result-grid">${results.map(gameCard).join('')}</div>`:`<div class="empty">${icon('search')}<h3>No matches yet</h3><p>Try another search term or choose a different genre.</p><button type="button" class="btn btn-outline" data-action="clear-filters">Clear filters</button></div>`;
  }
  function renderBrowse(){
    $('#main').innerHTML=`<div class="page-heading"><div><div class="kicker">EXPLORE THE STORE</div><h1>Find your next favourite.</h1><p>Clear filters, recognisable categories and straightforward game information — designed for newcomers and returning players.</p></div></div>
    <div class="browse-layout"><aside class="filters" aria-label="Filter games"><h3>${icon('sliders')} Browse filters</h3><div class="filter-heading">GENRE</div><div class="filter-group" role="radiogroup" aria-label="Genre">${genres.map(g=>`<label><input name="genre" type="radio" value="${g}" ${browse.genre===g?'checked':''}>${g}</label>`).join('')}</div><div class="filter-heading">SEARCH</div><label for="browse-query" style="display:block;font-size:12px;color:#a7becd;margin-bottom:6px">Game title or tag</label><input class="field" style="width:100%" type="search" id="browse-query" value="${htmlSafe(browse.query)}" placeholder="Search games"><button type="button" class="library-minor-action" style="margin-top:14px" data-action="clear-filters">Clear all filters</button></aside>
    <div><div class="control-row"><span id="result-count" aria-live="polite" style="font-size:12px;color:var(--muted)"></span><label class="sort-label" for="sort-select">Sort by <select class="select" id="sort-select"><option value="popular">Featured order</option><option value="rated">Highest rated</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option></select></label></div><div id="browse-results"></div></div></div>`;
    $('#sort-select').value=browse.sort;updateBrowseResults();
  }
  function renderGame(){
    const id=new URLSearchParams(location.search).get('id');const g=byId(id)||GAMES[0];
    document.title=`${g.title} | Steam Reimagined`;
    const related=GAMES.filter(x=>x.id!==g.id&&(x.genre===g.genre||x.tags.some(t=>g.tags.includes(t)))).slice(0,4);
    $('#main').innerHTML=`<p><a href="browse.html" class="text-link">${icon('arrow-left')} Back to discovery</a></p><div class="detail-hero" style="margin-top:21px"><div class="detail-visual"><img src="${art(g)}" width="1200" height="750" alt="Original concept artwork for ${htmlSafe(g.title)}"></div><div class="detail-side"><div class="kicker">${htmlSafe(g.badge)}</div><h1>${htmlSafe(g.title)}</h1><p>${htmlSafe(g.description)}</p><div class="detail-tags">${g.tags.map(t=>`<span>${htmlSafe(t)}</span>`).join('')}</div><div style="color:var(--lime);font-size:12px;font-weight:850">${g.rating}% positive · Fictional rating for demonstration</div><div class="detail-price">${g.oldPrice?`<span class="old-price" style="font-size:16px">${money(g.oldPrice)}</span> `:''}${money(g.price)} <span style="font-size:12px;color:var(--muted);font-weight:400">AUD · Demo store</span></div><div class="detail-buttons">${cartButton(g,true)}${wishlistButton(g,true)}</div><div class="detail-facts"><div><span>Developer</span><span>${htmlSafe(g.studio)}</span></div><div><span>Release</span><span>${g.release}</span></div><div><span>Genre</span><span>${htmlSafe(g.genre)}</span></div><div><span>Features</span><span>${g.features.map(htmlSafe).join(', ')}</span></div></div></div></div>
    ${sectionHeader('A closer look','Original concept visuals, created for this student project.')}
    <div class="media-row"><figure><img src="${art(g)}" loading="lazy" width="1200" height="750" alt="Artwork overview"><figcaption>Cover artwork</figcaption></figure><figure><img src="${art(GAMES[(GAMES.indexOf(g)+3)%GAMES.length])}" loading="lazy" width="1200" height="750" alt="Secondary concept artwork"><figcaption>Environment mood reference</figcaption></figure><figure><img src="${art(GAMES[(GAMES.indexOf(g)+6)%GAMES.length])}" loading="lazy" width="1200" height="750" alt="Additional concept artwork"><figcaption>Visual design reference</figcaption></figure></div>
    ${sectionHeader('You might also like','Discover games with similar themes.','browse.html','Browse more')}<div class="game-grid">${(related.length?related:GAMES.slice(0,4)).map(gameCard).join('')}</div>`;
  }
  function emptyContent(name,description,href,label){return `<div class="empty">${icon(name==='Wishlist'?'heart':'cart')}<h3>Your ${name.toLowerCase()} is empty</h3><p>${description}</p><a class="btn btn-primary" href="${href}">${label} ${icon('arrow-right')}</a></div>`;}
  function renderWishlist(){
    const games=GAMES.filter(g=>state.wishlist.has(g.id));
    $('#main').innerHTML=`<div class="page-heading"><div><div class="kicker">SAVED FOR LATER</div><h1>Your wishlist <span class="wishlist-counter"></span></h1><p>Keep track of the games you care about, without cluttering your store experience.</p></div><a href="browse.html" class="btn btn-outline">${icon('plus')} Find games</a></div>${games.length?`<div class="game-grid">${games.map(gameCard).join('')}</div>`:emptyContent('Wishlist','Save games as you browse and find them here whenever you return.','browse.html','Browse games')}`;
    updateCounts();
  }
  function renderCart(){
    const games=GAMES.filter(g=>state.cart.has(g.id));const total=games.reduce((sum,g)=>sum+g.price,0);
    $('#main').innerHTML=`<div class="page-heading"><div><div class="kicker">REVIEW YOUR SELECTION</div><h1>Shopping cart <span class="cart-counter"></span></h1><p>A transparent, simple review step. This is a student demonstration — no actual payments or accounts.</p></div></div>${games.length?`<div class="cart-layout"><div class="item-list">${games.map(g=>`<article class="list-item"><img src="${art(g)}" alt="Artwork for ${htmlSafe(g.title)}" width="1200" height="750"><div><h3><a href="game.html?id=${g.id}">${htmlSafe(g.title)}</a></h3><small>${htmlSafe(g.genre)}</small><span class="pill">${icon('check')} Digital download · demo</span></div><div class="list-actions"><strong class="price">${money(g.price)}</strong><button type="button" class="btn btn-neutral" data-action="remove-cart" data-id="${g.id}">${icon('trash')} Remove</button></div></article>`).join('')}</div><aside class="summary"><h2>Order summary</h2><div class="summary-row"><span>Games (${games.length})</span><strong>${money(total)}</strong></div><div class="summary-row"><span>Estimated total</span><strong>${money(total)}</strong></div><button type="button" class="btn btn-primary" data-action="checkout">Continue to demo checkout ${icon('arrow-right')}</button><p>${icon('shield')} This prototype never requests card details or processes payments.</p></aside></div>`:emptyContent('Cart','Add a game from the store, and you can review it here.','browse.html','Explore the store')}`;
    updateCounts();
  }
  function renderLibrary(){
    const owned=[GAMES[0],GAMES[1],GAMES[2]];
    $('#main').innerHTML=`<div class="page-heading"><div><div class="kicker">YOUR COLLECTION</div><h1>Library.</h1><p>A quiet home for your games. This is a fictional collection demonstrating a simplified library layout.</p></div><a class="btn btn-outline" href="browse.html">${icon('search')} Discover more</a></div>
    ${sectionHeader('Recently played','Pick up where you left off.')}<div class="library-tiles">${owned.map((g,i)=>`<article class="library-tile"><img src="${art(g)}" alt="${htmlSafe(g.title)} artwork" loading="lazy" width="1200" height="750"><div class="game-copy"><h3 style="margin:0">${htmlSafe(g.title)}</h3><small>${['Last played yesterday','Last played 3 days ago','Last played last week'][i]}</small><button type="button" class="btn btn-neutral" data-action="launch-demo" data-id="${g.id}">${icon('gamepad')} Play (demo)</button></div></article>`).join('')}</div>
    <section class="library-secondary" aria-labelledby="other-games"><h2 id="other-games">Other games</h2><p style="font-size:13px;color:var(--muted)">Non-Steam titles are secondary to your library, so the option to add them lives here — not as a prominent Store action.</p><div class="nonsteam-list" id="nonsteam-list"></div><div class="library-footer"><button class="library-minor-action" data-action="add-nonsteam" type="button">${icon('plus')} Add a non-Steam game</button></div></section>`;
    renderNonsteam();
  }
  function renderNonsteam(){
    const target=$('#nonsteam-list');if(!target)return;
    target.replaceChildren();
    if(!state.nonsteam.length){const p=document.createElement('p');p.textContent='No non-Steam games added.';p.style.cssText='font-size:12px;color:var(--soft)';target.appendChild(p);return;}
    state.nonsteam.forEach((name,i)=>{
      const el=document.createElement('div');el.className='nonsteam-entry';
      const label=document.createElement('span');label.textContent=name;
      const btn=document.createElement('button');btn.type='button';btn.dataset.action='remove-nonsteam';btn.dataset.index=String(i);btn.setAttribute('aria-label',`Remove ${name}`);btn.innerHTML=icon('x');
      el.append(label,btn);target.appendChild(el);
    });
  }
  function renderPage(){
    if(PAGE==='home')renderHome();else if(PAGE==='browse')renderBrowse();else if(PAGE==='game')renderGame();else if(PAGE==='wishlist')renderWishlist();else if(PAGE==='cart')renderCart();else if(PAGE==='library')renderLibrary();
    updateCounts();
  }
  function updateActionButtons(){
    $$('[data-action="wishlist"],[data-action="cart"]').forEach(old=>{
      const g=byId(old.dataset.id);if(!g)return;
      const isWishlist=old.dataset.action==='wishlist';
      const span=old.closest('.small-actions')===null;
      const wrap=document.createElement('div');wrap.innerHTML=isWishlist?wishlistButton(g,span):cartButton(g,span);
      old.replaceWith(wrap.firstChild);
    });
  }
  function handleToggle(action,id){
    const g=byId(id);if(!g)return;
    const set=action==='wishlist'?state.wishlist:state.cart;
    const was=set.has(id);was?set.delete(id):set.add(id);saveCollections();
    toast(`${g.title} ${was?'removed from':'added to'} ${action==='cart'?'cart':'wishlist'}.`);
    if(PAGE==='wishlist'||PAGE==='cart')renderPage();else updateActionButtons();
  }
  function openDialog(selector){const dialog=$(selector);if(dialog&&!dialog.open){dialog.showModal();}}
  function searchSuggestions(input){
    const target=$('#search-suggestions');if(!target)return;
    const value=input.value.trim().toLowerCase();
    if(value.length<2){target.classList.remove('open');target.replaceChildren();return;}
    const games=GAMES.filter(g=>g.title.toLowerCase().includes(value)||g.tags.some(x=>x.toLowerCase().includes(value))).slice(0,4);
    target.innerHTML=games.map(g=>`<a class="suggestion" href="game.html?id=${g.id}"><img src="${art(g)}" width="1200" height="750" alt=""><span>${htmlSafe(g.title)}<small>${htmlSafe(g.genre)} · ${money(g.price)}</small></span></a>`).join('') || '<div style="padding:10px;color:#bbccd8;font-size:12px">No quick matches — press Enter to search.</div>';
    target.classList.add('open');
  }
  function setup(){
    $$('.nav-main a, .side-link').forEach(link=>{const path=(location.pathname.split('/').pop()||'index.html');if(link.getAttribute('href')===path)link.classList.add('active');});
    updateCounts();renderPage();
    const friend=$('#friends-dock'), toggle=$('#friends-toggle');
    toggle.addEventListener('click',()=>{const open=!friend.classList.contains('is-open');friend.classList.toggle('is-open',open);toggle.setAttribute('aria-expanded',String(open));});
    $('#menu-toggle').addEventListener('click',()=>{const open=document.body.classList.toggle('menu-open');$('#menu-toggle').setAttribute('aria-expanded',String(open));});
    const globalSearch=$('#global-search');globalSearch.addEventListener('input',()=>searchSuggestions(globalSearch));
    globalSearch.addEventListener('keydown',e=>{if(e.key==='Escape'){$('#search-suggestions').classList.remove('open');globalSearch.blur();}});
    document.addEventListener('click',e=>{
      if(!e.target.closest('.search-form'))$('#search-suggestions').classList.remove('open');
      const btn=e.target.closest('[data-action]');if(!btn)return;
      const action=btn.dataset.action,id=btn.dataset.id;
      if(action==='wishlist'||action==='cart'){handleToggle(action,id);return;}
      if(action==='remove-cart'){handleToggle('cart',id);return;}
      if(action==='collapse'){
        const panel=$(`#shelf-${id}`);if(!panel)return;const collapsed=panel.classList.toggle('collapsed');
        collapsed?state.collapsed.add(id):state.collapsed.delete(id);writeStore('collapsed',[...state.collapsed]);
        btn.setAttribute('aria-expanded',String(!collapsed));btn.setAttribute('aria-label',`${collapsed?'Expand':'Collapse'} ${$('#shelf-title-'+id).textContent}`);return;
      }
      if(action==='customize'){
        ['recommended','offers','popular'].forEach(x=>{const control=$(`#shelf-pref-${x}`);if(control)control.checked=!state.hiddenShelves.has(x);});openDialog('#customize-dialog');return;
      }
      if(action==='clear-filters'){browse={query:'',genre:'All',sort:'popular'};try{history.replaceState(null,'','browse.html');}catch{/* Navigation-restricted preview contexts */}renderBrowse();return;}
      if(action==='checkout'){openDialog('#checkout-dialog');return;}
      if(action==='add-nonsteam'){openDialog('#nonsteam-dialog');$('#nonsteam-title').focus();return;}
      if(action==='remove-nonsteam'){
        const index=Number(btn.dataset.index);if(!Number.isInteger(index)||index<0||index>=state.nonsteam.length)return;
        const removed=state.nonsteam.splice(index,1)[0];writeStore('nonsteam',state.nonsteam);renderNonsteam();toast(`${removed} removed from the Library.`);return;
      }
      if(action==='launch-demo'){toast('This is a UI prototype; no actual game is installed.');return;}
      if(action==='close-modal'){btn.closest('dialog')?.close();return;}
    });
    document.addEventListener('change',e=>{
      if(e.target.matches('input[name="genre"]')){browse.genre=e.target.value;updateBrowseResults();}
      if(e.target.id==='sort-select'){browse.sort=e.target.value;updateBrowseResults();}
    });
    document.addEventListener('input',e=>{if(e.target.id==='browse-query'){browse.query=e.target.value;updateBrowseResults();}});
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'){document.body.classList.remove('menu-open');$('#menu-toggle').setAttribute('aria-expanded','false');friend.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');}
    });
    $('#customize-form').addEventListener('submit',e=>{
      e.preventDefault();state.hiddenShelves.clear();['recommended','offers','popular'].forEach(x=>{if(!$('#shelf-pref-'+x).checked)state.hiddenShelves.add(x);});
      writeStore('hiddenShelves',[...state.hiddenShelves]);$('#customize-dialog').close();if(PAGE==='home')renderHome();toast('Your shelf preferences are saved.');
    });
    $('#nonsteam-form').addEventListener('submit',e=>{
      e.preventDefault();const input=$('#nonsteam-title'),err=$('#nonsteam-error');const name=input.value.trim().replace(/\s+/g,' ');
      if(name.length<2||name.length>36){err.textContent='Please use a game name between 2 and 36 characters.';return;}
      if(state.nonsteam.some(x=>x.toLowerCase()===name.toLowerCase())){err.textContent='That game is already in your Library.';return;}
      if(state.nonsteam.length>=20){err.textContent='The demonstration Library holds up to 20 additional titles.';return;}
      err.textContent='';state.nonsteam.push(name);writeStore('nonsteam',state.nonsteam);$('#nonsteam-dialog').close();input.value='';renderNonsteam();toast(`${name} added to your Library.`);
    });
  }
  document.addEventListener('DOMContentLoaded',setup);
})();
