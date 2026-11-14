class StockPortfolioCard extends HTMLElement {
 setConfig(config){if(!Array.isArray(config.stocks))throw Error("stocks is required");this.config=config;if(!this.shadowRoot)this.attachShadow({mode:"open"});this.draw();}
 set hass(hass){this._hass=hass;if(this.config)this.draw();}
 getCardSize(){return 3;}
 draw(){
 const e=x=>String(x??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
 const num=(entity,attr)=>{const s=this._hass?.states?.[entity];const v=attr?s?.attributes?.[attr]:s?.state;return v===null||v===undefined||v===""||!Number.isFinite(Number(v))?null:Number(v)};
 const fmt=(v,d=2)=>v===null?"—":Number(v).toLocaleString("en-US",{minimumFractionDigits:d,maximumFractionDigits:d});
 const showVolume=this.config.show_volume===true;
 const rows=this.config.stocks.map(s=>{
 const price=num(s.entity); const change=num(s.entity,s.change_attribute||"change_pct") ?? num(s.entity,"regularMarketChangePercent"); const vol=num(s.entity,s.volume_attribute||"regularMarketVolume");
 const shares=Number(s.shares),basis=Number(s.basis);
 const holding=s.shares!==undefined&&s.basis!==undefined&&Number.isFinite(shares)&&Number.isFinite(basis)&&shares>0&&basis>=0;
 const gain=price!==null&&holding?(price-basis)*shares:null;
 const gainAmount=Number.isFinite(gain)?fmt(Math.abs(gain)):null;
 const gainColor=gainAmount===null||gainAmount==="0.00"?"":gain>0?"positive":"negative";
 const gainText=gainAmount===null?"—":(gainColor==="positive"?"+":gainColor==="negative"?"-":"")+"$"+gainAmount;
 const dayColor=change===null?"":change>=0?"positive":"negative";
 return `<tr><th>${e(s.name||s.ticker||s.entity)}<small>${e(s.ticker||"")}</small></th><td>${price===null?"No quote":"$"+fmt(price)}</td><td class="${dayColor}">${change===null?"—":(change>0?"+":"")+fmt(change)+"%"}</td>${showVolume?`<td>${fmt(vol,0)}</td>`:""}<td class="${gainColor}">${gainText}</td></tr>`;
 }).join("");
 this.shadowRoot.innerHTML=`<style>ha-card{padding:10px;overflow:hidden}h2{margin:0 0 12px;font-size:16px}.wrap{overflow-x:auto;container-type:inline-size}table{display:grid;width:100%;grid-template-columns:max-content repeat(2,minmax(max-content,1fr)) 12px minmax(max-content,1fr);border-spacing:0}table.with-volume{grid-template-columns:max-content repeat(3,minmax(max-content,1fr)) 12px minmax(max-content,1fr)}thead,tbody,tr{display:grid;grid-column:1/-1;grid-template-columns:subgrid}th,td{padding:7px 2px;text-align:right;border-bottom:1px solid var(--divider-color);font-size:12px}th:first-child{text-align:left;white-space:nowrap}th:not(:first-child),td{padding-inline:1px;white-space:nowrap}td{font-variant-numeric:tabular-nums}tr>:last-child{grid-column:-2/-1}thead th{font-size:10px;opacity:.7;text-transform:uppercase}@container (min-width:340px){tbody th,td{font-size:14px}thead th{font-size:12px}}small{display:block;opacity:.6;font-weight:400}.positive{color:#35c987;font-weight:700}.negative{color:#f46d78;font-weight:700}</style><ha-card><h2>${e(this.config.title||"My Stocks")}</h2><div class="wrap"><table class="${showVolume?"with-volume":""}"><thead><tr><th>Stock</th><th>Price</th><th>Day %</th>${showVolume?"<th>Volume</th>":""}<th>Gain/Loss ($)</th></tr></thead><tbody>${rows}</tbody></table></div></ha-card>`;
 }
}
if(!customElements.get("stock-portfolio-card"))customElements.define("stock-portfolio-card",StockPortfolioCard);
window.customCards=window.customCards||[];
window.customCards.push({type:"stock-portfolio-card",name:"Stock Portfolio Card",description:"Quotes and color-coded unrealized gains and losses"});
