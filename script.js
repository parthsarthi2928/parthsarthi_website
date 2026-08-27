
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

const glow = document.querySelector(".cursor-glow");
window.addEventListener("pointermove", (e) => {
  glow.style.left = e.clientX + "px";
  glow.style.top = e.clientY + "px";
});

document.getElementById("year").textContent = new Date().getFullYear();

const cases = {
  idiscover: {
    kicker: "CASE STUDY · IDISCOVER",
    title: "Enterprise data platform architecture",
    text: "Architected a unified enterprise data platform spanning ingestion, warehouse design and downstream data distribution, with reusable engineering patterns for scale.",
    bullets: [
      "Designed metadata-driven, reusable and restartable ETL capabilities.",
      "Architected AWS-based orchestration and warehouse patterns using Airflow, Redshift and PostgreSQL.",
      "Applied dimensional modelling patterns across enterprise analytical domains.",
      "Improved delivery reliability through CI/CD, testing automation and IAM-based security."
    ]
  },
  angen: {
    kicker: "CASE STUDY · ANGEN",
    title: "Analytics architecture on enterprise foundations",
    text: "Designed an analytics architecture on top of the enterprise warehouse to support advanced analytics and self-service consumption.",
    bullets: [
      "Translated analytical requirements into data models, aggregation strategies and consumption-layer designs.",
      "Governed data quality, reliability and SLA adherence across platform boundaries.",
      "Aligned business stakeholders and engineering teams around implementable platform decisions."
    ]
  },
  modern: {
    kicker: "CURRENT INITIATIVE",
    title: "Modernising toward Databricks",
    text: "Supporting the migration of data orchestration and processing workloads toward a modern, scalable and managed Databricks engineering architecture.",
    bullets: [
      "Evolving platform orchestration and processing patterns.",
      "Applying managed data engineering capabilities to improve scalability and maintainability.",
      "Modernising while preserving enterprise reliability and delivery accountability."
    ]
  }
};

const dlg = document.getElementById("case-modal");
const content = document.getElementById("modal-content");
document.querySelectorAll("[data-modal]").forEach(btn => {
  btn.addEventListener("click", () => {
    const c = cases[btn.dataset.modal];
    content.innerHTML = `<div class="modal-body"><p class="kicker">${c.kicker}</p><h2>${c.title}</h2><p>${c.text}</p><ul>${c.bullets.map(x=>`<li>${x}</li>`).join("")}</ul></div>`;
    dlg.showModal();
  });
});
document.querySelector(".modal-close").addEventListener("click",()=>dlg.close());
dlg.addEventListener("click",(e)=>{ if(e.target === dlg) dlg.close(); });
