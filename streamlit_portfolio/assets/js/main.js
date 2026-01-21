// year in footer
document.getElementById('y')?.appendChild(document.createTextNode(new Date().getFullYear()));

// tiny scroll reveal
const observer = new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){ e.target.classList.add('active'); observer.unobserve(e.target); }
  });
},{threshold:0.12});

document.querySelectorAll('.tile, .about-card, .hero, .pill').forEach(el=>{
  el.classList.add('reveal');
  observer.observe(el);
});
