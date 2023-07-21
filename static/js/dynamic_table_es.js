let sectionCount = 0;

function addBuildingSection() {
  const buildingSectionsDiv = document.getElementById('building-sections');

  // 建立新的建物分區小表單
  const sectionForm = document.createElement('div');
  sectionForm.id = `section-${sectionCount}`;
  sectionForm.innerHTML = `

    <div class="form-line">

        <div class="form-label">建物耗能分區</div>

        <select class="form-input-1" name="es-id-${sectionCount}">
          <option value="A1">A1. 小型護理或長照機構</option>
          <option value="A2">A2. 小型日照機構、幼兒園</option>
          <option value="A3">A3. 值班宿舍或招待所</option>
          <option value="A4">A4. 學生宿舍（有寒暑假之學校住宿）</option>
          <option value="A5">A5. 出租宿舍或民宿</option>
          <option value="B1">B1. 企業商辦大樓企業商辦大樓（五都主要商圈，中央空調、大銀行或大國際品牌企業進駐、大廳有大訪客休息區）</option>
          <option value="B2">B2. 企業商辦大樓專用大廳或專用走廊休息區等次空間</option>
          <option value="B3">B3. 一般辦公大樓（一般商辦、政府辦公、分租型辦公）</option>
          <option value="B4">B4. 一般辦公大樓專用大廳或專用走廊休息區等次空間</option>
          <option value="C1">C1. 國家圖書館或六都總圖書館之書庫／閱覽區</option>
          <option value="C2">C2. 國家圖書館或六都總圖書館之大廳（含動態展區與休息廳）</option>
          <option value="C3">C3. 國家圖書館或六都總圖書館或大學總圖書館之行政辦公區</option>
          <option value="C4">C4. C1 以外圖書館之書庫／閱覽區</option>
          <option value="C5">C5. C1 以外圖書館之大廳（含動態展區與休息廳）</option>
          <option value="C6">C6. C1 以外圖書館之行政辦公區</option>
          <option value="C7">C7. 大學總圖書館之書庫／閱覽區</option>
          <option value="C8">C8. 大學總圖書館之大廳（含動態展區與休息廳）</option>
          <option value="D1">D1. A 級全天空調展覽區（低溼控制）</option>
          <option value="D2">D2. B 級全天空調展覽區</option>
          <option value="D3">D3. B 級營業時間內空調展覽區</option>
          <option value="D4">D4. 展覽類行政辦公區</option>
          <option value="D5">D5. 大廳</option>
          <option value="E1">E1. 出租展覽區</option>
          <option value="E2">E2. 行政辦公區</option>
          <option value="E3">E3. 大廳</option>
          <option value="F1">F1. 200 人以上體育館、大會議廳與其專屬大廳</option>
          <option value="F2">F2. 少於 200 人之體育館、中小型會議廳或藝文教室與其專屬門廳走廊</option>
          <option value="F3">F3. 體育館、演講中心行政辦公區</option>
          <option value="F4">F4. 大廳</option>
          <option value="G1">G1. 國家級演藝廳與其專屬門廳走廊</option>
          <option value="G2">G2. 一般級別演藝廳與其專屬門廳走廊</option>
          <option value="H1">H1. 飯店客房區</option>
          <option value="H2">H2. 飯店客房區（冬季供暖房型）</option>
          <option value="H3">H3. 飯店 8 小時一般行政辦公區</option>
          <option value="H4">H4. 飯店餐飲宴會部行政辦公區</option>
          <option value="H5">H5. 客房設施部維管辦公區</option>
          <option value="H6">H6. 飯店櫃台接待大廳休息區</option>
          <option value="H7">H7. 員工休息、盥洗室</option>
          <option value="H8">H8. 飯店附設泳池</option>
          <option value="H9">H9. 飯店附設運動中心</option>
          <option value="H10">H10. 宴會廳（主要以宴客為主，不含專用廚房，以 I2 餐之 70% 計）</option>
          <option value="I1">I1. 供一餐餐廳用餐區（不含專用廚房）</option>
          <option value="I2">I2. 供午晚兩餐餐廳用餐區（不含專用廚房）</option>
          <option value="I3">I3. 供三餐餐廳用餐區（不含專用廚房）</option>
          <option value="I4">I4. 輕食類或咖啡廳用餐區（不含吧檯與廚房區）</option>
          <option value="I5">I5. 24 hr 餐廳用餐區（不含專用廚房）</option>
          <option value="I6">I6. 火鍋、燒烤店（含廚房）</option>
          <option value="I7">I7. 百貨商場美食街（不含專用廚房）</option>
          <option value="J1">J1. 12 小時一般商店、百貨專櫃、名店街</option>
          <option value="J2">J2. 12 小時高照明商場（精品專櫃區）</option>
          <option value="J3">J3. 24 hr 零售商店</option>
          <option value="J4">J4. 24 hr 高照明商場、便利商店（沿街型）</option>
          <option value="J5">J5. 15 小時超市、量販店一般貨品區</option>
          <option value="J6">J6. 超市、量販店冰櫃式冷凍冷藏生鮮區</option>
          <option value="J7">J7. 電影院、影城</option>
          <option value="J8">J8. 12 小時小鋼珠店、電子遊樂場</option>
          <option value="J9">J9. 24 小時 KTV</option>
          <option value="J10">J10. 24 小時網咖</option>
          <option value="K1">K1. 醫院病房區</option>
          <option value="K2">K2. 門診醫療空間或 G3 類之小醫院、私人診所</option>
          <option value="K3">K3. 24 小時加護病房區、急診部</option>
          <option value="K4">K4. 24 小時手術房區、檢驗部</option>
          <option value="K5">K5. 醫院大廳含掛號業務大廳</option>
          <option value="K6">K6. 醫院一般行政辦公區與設施維管區域</option>
          <option value="K7">K7. 腫瘤放射重設備</option>
          <option value="K8">K8. 護理或長照機構</option>
          <option value="K9">K9. 日照機構、幼兒園</option>
          <option value="L1">L1. 行政、辦公、設施維護管理區（使用率 100%）</option>
          <option value="L2">L2. 高樓層球類運動區（11 m 高，使用率 75%）</option>
          <option value="L3">L3. 體能調適運動區（健身房、使用率 100%）</option>
          <option value="L4-1">L4-1. 多功能教室（社區教室、棋藝閱覽室、兒童遊戲室、桌球室、撞球室，使用率 62.5%）</option>
          <option value="L4-2">L4-2. 多功能教室（韻律教室、飛輪教室、舞蹈教室、壁球室，使用率 75%）</option>
          <option value="L5">L5. 室內溜冰區（使用率 100%）</option>
          <option value="L6-1">L6-1. 全年溫水空調型游泳池</option>
          <option value="L6-2">L6-2. 季節溫水空調型游泳池</option>
          <option value="L6-3">L6-3. 通風無空調季節溫水游泳池</option>
          <option value="NB1">NB1. 國小教室（辦公區歸 B3）</option>
          <option value="NB2">NB2. 國中教室（辦公區歸 B3）</option>
          <option value="NB3">NB3. 高中職、大專教室、教師研究室（辦公區歸 B3）</option>
          <option value="NB4">NB4. 研究機構實驗室</option>
          <option value="NB5">NB5. 室內體育館（A-1）</option>
          <option value="NB6">NB6. 車站、轉運站、航站業務大廳（A-2）</option>
          <option value="NB7">NB7. 24 小時作業無空調一般工廠製程區（辦公區歸 B3）</option>
          <option value="NB8">NB8. 24 小時作業空調型一般工廠製程區（辦公區歸 B3）</option>
          <option value="NB9">NB9. 24 小時作業空調型精密或潔淨製造製程區（辦公區歸 B3）</option>
          <option value="NB10">NB10. 10 小時作業無空調一般工廠製程區（辦公區歸 B3）</option>
          <option value="NB11">NB11. 10 小時作業空調型一般工廠製程區（辦公區歸 B3）</option>
          <option value="NB12">NB12. 10 小時作業空調型精密或潔淨製造製程區（辦公區歸 B3）</option>
          <option value="NB13">NB13. 室內停車場</option>
          <option value="NB14">NB14. 無空調通風型專用倉儲</option>
          <option value="NB15">NB15. 空調型專用倉儲</option>
          <option value="R1">R1. 透天獨棟住宅</option>
          <option value="R2">R2. 透天連棟住宅</option>
          <option value="R3">R3. 非透天集合住宅住戶專用分區</option>
          <option value="P1">P1. 非透天集合住宅大廳分區（大廳空間）</option>
          <option value="P2">P2. 非透天集合住宅梯廳分區（梯廳與住戶連通走廊）</option>
          <option value="P3">P3. 非透天集合住宅之一般共用分區（健身房、閱覽室、兒童遊戲室、KTV、會議室、視聽室、社區辦公室、活動中心等）</option>
        </select>

        <div class="form-label">耗能分區屬性</div>

        <input class="form-input-1" type="text" placeholder="年使用時數" required name="es-attr-int-${sectionCount}">
        
        <button class="form-button-dynamic-delete" type="button" onclick="removeBuildingSection(${sectionCount})">刪除</button>
    
        </div>
  `;
  buildingSectionsDiv.appendChild(sectionForm);
  sectionCount++;
}

function removeBuildingSection(sectionIndex) {
  const buildingSectionsDiv = document.getElementById('building-sections');
  const sectionForm = document.querySelector(`#section-${sectionIndex}`);
  buildingSectionsDiv.removeChild(sectionForm);
}

const mainForm = document.getElementById('main-form');
mainForm.onsubmit = function(event) {
  event.preventDefault();
  // 在這裡處理主表單提交，將所有新增的建物分區資料收集並處理
  console.log("主表單提交：");
  const buildingSectionsDiv = document.getElementById('building-sections');
  const buildingSections = buildingSectionsDiv.children;
  for (const section of buildingSections) {
    console.log("建物分區名稱：", section.querySelector('input[type="text"][name^="name"]').value);
    console.log("建物分區屬性：", section.querySelector('input[type="text"][name^="attribute"]').value);
  }
};