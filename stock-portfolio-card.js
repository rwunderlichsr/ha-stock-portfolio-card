class StockPortfolioCard extends HTMLElement {
 setConfig(config){if(!Array.isArray(config.stocks))throw Error("stocks is required");this.config=config;if(!this.shadowRoot)this.attachShadow({mode:"open"});this.draw();}
 set hass(hass){this._hass=hass;if(this.config)this.draw();}
 getCardSize(){return 3;}
 draw(){
 const e=x=>String(x??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
 const num=(entity,attr)=>{const s=this._hass?.states?.[entity];const v=attr?s?.attributes?.[attr]:s?.state;return v===null||v===undefined||v===""||!Number.isFinite(Number(v))?null:Number(v)};
 const fmt=(v,d=2)=>v===null?"—":Number(v).toLocaleString("en-US",{minimumFractionDigits:d,maximumFractionDigits:d});
 const showBasis=this.config.show_cost_basis!==false; const showGL=this.config.show_gain_loss===true; const showVolume=this.config.show_volume===true;
 const rows=this.config.stocks.map(s=>{
 const price=num(s.entity); const change=num(s.entity,s.change_attribute||"change_pct") ?? num(s.entity,"regularMarketChangePercent"); const vol=num(s.entity,s.volume_attribute||"regularMarketVolume");
 const shares=Number(s.shares),basis=Number(s.basis),holding=s.shares!==undefined&&s.basis!==undefined&&shares>0&&basis>=0;
 const value=price!==null&&holding?price*shares:null;
 const gain=value===null?null:value-basis*shares;
 const dayColor=change===null?"":change>=0?"positive":"negative",valueColor=value===null?"":price>=basis?"positive":"negative";
 return `<tr><th>${e(s.ticker||s.name||s.entity)}</th><td>${price===null?"No quote":"$"+fmt(price)}</td><td class="${dayColor}">${change===null?"—":(change>0?"+":"")+fmt(change)+"%"}</td>${showVolume?`<td>${fmt(vol,0)}</td>`:""}${showBasis?`<td>${holding?"$"+fmt(basis):"—"}</td>`:""}<td class="${valueColor}">${value===null?"—":"$"+fmt(value)}</td>${showGL?`<td class="${valueColor}">${gain===null?"—":(gain>=0?"+":"-")+"$"+fmt(Math.abs(gain))}</td>`:""}</tr>`;
 }).join("");
 this.shadowRoot.innerHTML=`<style>ha-card{padding:10px;overflow:hidden}h2{margin:0 0 12px;font-size:16px}.wrap{overflow-x:auto}table{width:100%;min-width:0;table-layout:fixed;border-collapse:collapse}th,td{padding:7px 3px;text-align:right;border-bottom:1px solid var(--divider-color);font-size:11px}th:first-child{text-align:left;width:16%;overflow-wrap:anywhere}td{overflow-wrap:anywhere;font-variant-numeric:tabular-nums}thead th{font-size:9px;opacity:.7;text-transform:uppercase}small{display:block;opacity:.6;font-weight:400}.positive{color:#35c987;font-weight:700}.negative{color:#f46d78;font-weight:700}</style><ha-card><h2>${e(this.config.title||"My Stocks")}</h2><div class="wrap"><table><thead><tr><th>Stock</th><th>Price</th><th>Day %</th>${showVolume?"<th>Volume</th>":""}${showBasis?"<th>Avg basis</th>":""}<th>Market value</th>${showGL?"<th>Gain / loss</th>":""}</tr></thead><tbody>${rows}</tbody></table></div></ha-card>`;
 }
}
if(!customElements.get("stock-portfolio-card"))customElements.define("stock-portfolio-card",StockPortfolioCard);
window.customCards=window.customCards||[];
window.customCards.push({type:"stock-portfolio-card",name:"Stock Portfolio Card",description:"Quotes and color-coded holding values"});
