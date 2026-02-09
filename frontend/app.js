console.log("CLIMA frontend loaded");

let incidentHistory = [];

async function loadIncident(){

 try{

   const res = await fetch("http://localhost:8000/incident");
   const data = await res.json();

   if(!data.intelligence || !data.response) return;

   document.getElementById("incident").innerText =
     data.intelligence.incident_type || "—";

   document.getElementById("confidence").innerText =
     data.intelligence.confidence || "—";

   const sev = document.getElementById("severity");
   sev.innerText = data.response.severity || "—";
   sev.className="";

   if(sev.innerText.toUpperCase().includes("CRITICAL")){
     sev.classList.add("critical");
   }

   document.getElementById("status").innerText =
     " Updated " + new Date().toLocaleTimeString();

   document.getElementById("graph").innerHTML="";
   document.getElementById("timeline").innerHTML="";
   document.getElementById("map").innerHTML="";

   drawGraph(data.graph.nodes || []);
   drawAQI();
   drawMap();

   if(data.response.mitigation_steps)
     drawTimeline(data.response.mitigation_steps);

   // Incident history
   incidentHistory.unshift({
     time:new Date().toLocaleTimeString(),
     type:data.intelligence.incident_type
   });

   incidentHistory = incidentHistory.slice(0,5);

   const h=document.getElementById("history");
   h.innerHTML="";
   incidentHistory.forEach(i=>{
     h.innerHTML += `<div>${i.time} — ${i.type}</div>`;
   });

 }catch(e){
   console.error("UI Error:",e);
 }
}

/* Causal Graph */

function drawGraph(nodes){

 let visNodes = nodes.map((n,i)=>({
   id:i,
   label:n,
   shape:"box",
   widthConstraint:{maximum:300},
   margin:10,
   color:{
     background:"#238636",
     border:"#2ecc71"
   },
   font:{
     color:"white",
     size:16,
     multi:true
   }
 }));

 let edges=[];

 for(let i=0;i<nodes.length-1;i++){
   edges.push({
     from:i,
     to:i+1,
     arrows:"to",
     color:"#2ecc71",
     smooth:true
   });
 }

 new vis.Network(
   document.getElementById("graph"),
   {
     nodes:new vis.DataSet(visNodes),
     edges:new vis.DataSet(edges)
   },
   {
     layout:{
       hierarchical:{
         enabled:true,
         direction:"UD",
         nodeSpacing:150,
         levelSeparation:100
       }
     },
     physics:false
   }
 );
}


/* AQI Chart */

function drawAQI(){

 const ctx=document.getElementById("aqiChart").getContext("2d");

 new Chart(ctx,{
  type:'line',
  data:{
   labels:["T-3","T-2","T-1","Now"],
   datasets:[{
    label:"PM2.5 (µg/m³)",
    data:[180,210,250,290],
    borderColor:"#ff4757",
    backgroundColor:"rgba(255,71,87,.3)",
    fill:true,
    tension:.4,
    pointRadius:6
   }]
  },
  options:{
   plugins:{
     legend:{labels:{color:"white"}}
   },
   scales:{
     x:{
       ticks:{color:"white"},
       title:{display:true,text:"Time",color:"white"}
     },
     y:{
       ticks:{color:"white"},
       title:{display:true,text:"PM2.5 µg/m³",color:"white"},
       grid:{color:"rgba(255,255,255,.1)"},
       suggestedMax:320
     }
   }
  }
 });
}

/* Map */

function drawMap(){

 let map=L.map('map').setView([29.1,76.8],7);

 L.tileLayer(
 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
 ).addTo(map);

 L.circle([29.1,76.8],{
   radius:25000,
   color:"red",
   fillColor:"#ff4757",
   fillOpacity:0.4
 }).addTo(map).bindPopup("Fire Hotspot");
}


/* Timeline */

function drawTimeline(steps){
 steps.forEach(s=>{
   let div=document.createElement("div");
   div.className="timeline";
   div.innerText=s;
   document.getElementById("timeline").appendChild(div);
 });
}

loadIncident();
setInterval(loadIncident,20000);
