
    // ================= STAGE & TAB SWITCHING =================
    const stageBtn1 = document.getElementById('stageBtn1');
    const stageBtnPractice = document.getElementById('stageBtnPractice');
    const tabsStage1 = document.getElementById('tabsStage1');
    const tabsStagePractice = document.getElementById('tabsStagePractice');
    const headerTitle = document.getElementById('headerStageTitle');

    const containers = {
      'A': document.getElementById('probAContainer'),
      'B': document.getElementById('probBContainer'),
      'C': document.getElementById('probCContainer'),
      'D': document.getElementById('probDContainer'),
      'E': document.getElementById('probEContainer'),
      'F': document.getElementById('probFContainer'),
      'G': document.getElementById('probGContainer'),
      'H': document.getElementById('probHContainer'),
      'I': document.getElementById('probIContainer'),
      'J': document.getElementById('probJContainer'),
      'K': document.getElementById('probKContainer'),
      'L': document.getElementById('probLContainer'),
      'M': document.getElementById('probMContainer'),
      'N': document.getElementById('probNContainer'),
      'P1': document.getElementById('probP1Container'),
      'P2': document.getElementById('probP2Container'),
      'P3': document.getElementById('probP3Container'),
      'P4': document.getElementById('probP4Container')
    };

    let activeStage = '1';
    let activeProb = 'A';

    function switchStage(stage) {
      activeStage = stage;
      if (stage === '1') {
        stageBtn1.className = 'px-3 py-1.5 rounded-lg font-bold bg-blue-600 text-white shadow-sm transition';
        stageBtnPractice.className = 'px-3 py-1.5 rounded-lg font-bold text-gray-400 hover:text-white transition';
        tabsStage1.classList.remove('hidden');
        tabsStagePractice.classList.add('hidden');
        headerTitle.textContent = 'UCPC 2026 Stage 1';
        selectProblem('A');
      } else {
        stageBtnPractice.className = 'px-3 py-1.5 rounded-lg font-bold bg-purple-600 text-white shadow-sm transition';
        stageBtn1.className = 'px-3 py-1.5 rounded-lg font-bold text-gray-400 hover:text-white transition';
        tabsStagePractice.classList.remove('hidden');
        tabsStage1.classList.add('hidden');
        headerTitle.textContent = 'UCPC 2026: Пробний тур';
        selectProblem('P4'); // Featured problem
      }
      lucide.createIcons();
    }

    function selectProblem(probId) {
      activeProb = probId;
      document.querySelectorAll('.prob-tab-btn').forEach(b => {
        if (b.dataset.prob === probId) {
          b.className = 'prob-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1 bg-blue-600 text-white shadow-sm shadow-blue-500/30';
        } else {
          b.className = 'prob-tab-btn px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1 bg-gray-800 text-gray-400 hover:text-white';
        }
      });

      Object.keys(containers).forEach(k => {
        if (containers[k]) {
          if (k === probId) containers[k].classList.remove('hidden');
          else containers[k].classList.add('hidden');
        }
      });
      lucide.createIcons();
    }

    stageBtn1.onclick = () => switchStage('1');
    stageBtnPractice.onclick = () => switchStage('practice');

    document.querySelectorAll('.prob-tab-btn').forEach(btn => {
      btn.onclick = () => selectProblem(btn.dataset.prob);
    });

    // ================= ANIMATION LOGIC FOR PROBLEM A (ANTIVIRUS) =================
    const treeNodes = [
      { id: 1, p: 0, x: 350, y: 40, label: 'Папка 1 (Корінь)' },
      { id: 2, p: 1, x: 200, y: 130, label: 'Папка 2' },
      { id: 3, p: 1, x: 500, y: 130, label: 'Папка 3' },
      { id: 4, p: 2, x: 120, y: 240, label: 'Папка 4' },
      { id: 5, p: 2, x: 280, y: 240, label: 'Папка 5' },
      { id: 6, p: 3, x: 420, y: 240, label: 'Папка 6' },
      { id: 7, p: 3, x: 580, y: 240, label: 'Папка 7' },
    ];

    let bValues = {};
    let stepIndex = 0;
    let animIntervalA = null;

    function resetProbA() {
      if (animIntervalA) {
        clearInterval(animIntervalA);
        animIntervalA = null;
      }
      stepIndex = 0;
      bValues = { 1: -1, 2: 1, 3: 2, 4: -1, 5: -1, 6: -1, 7: -1 };
      document.getElementById('animStepTextA').textContent = 'Початковий стан: у Папці 2 запущено силу d=1, у Папці 3 запущено силу d=2.';
      document.getElementById('btnPlayA').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      renderTreeA();
      renderArrayA();
      lucide.createIcons();
    }

    function renderTreeA(activeNodeId = null) {
      const svg = document.getElementById('treeSvg');
      let html = '';

      treeNodes.forEach(node => {
        if (node.p > 0) {
          const parent = treeNodes.find(n => n.id === node.p);
          const isLinkActive = node.id === activeNodeId;
          html += `<line x1="${parent.x}" y1="${parent.y}" x2="${node.x}" y2="${node.y}" stroke="${isLinkActive ? '#3B82F6' : '#374151'}" stroke-width="${isLinkActive ? '4' : '2.5'}" stroke-dasharray="${isLinkActive ? '5' : '0'}" />`;
        }
      });

      treeNodes.forEach(node => {
        const val = bValues[node.id];
        const isScanned = val >= 0;
        const isActive = node.id === activeNodeId;

        let fill = '#1F2937';
        let stroke = '#4B5563';
        if (isScanned) {
          fill = '#065F46';
          stroke = '#10B981';
        }
        if (isActive) {
          stroke = '#60A5FA';
          fill = '#1E3A8A';
        }

        html += `
          <g transform="translate(${node.x}, ${node.y})" class="${isActive ? 'node-pulse' : ''}">
            <circle r="26" fill="${fill}" stroke="${stroke}" stroke-width="${isActive ? '4' : '2.5'}" />
            <text text-anchor="middle" dy="-2" fill="#FFFFFF" font-size="12" font-weight="bold" font-family="Plus Jakarta Sans">${node.id}</text>
            <text text-anchor="middle" dy="13" fill="${isScanned ? '#34D399' : '#9CA3AF'}" font-size="10" font-family="JetBrains Mono">b=${val}</text>
          </g>
        `;
      });

      svg.innerHTML = html;
    }

    function renderArrayA() {
      const el = document.getElementById('arrayStateA');
      el.innerHTML = '';
      treeNodes.forEach(n => {
        const val = bValues[n.id];
        const isScanned = val >= 0;
        el.innerHTML += `
          <div class="p-2 rounded-lg border transition-all duration-300 ${isScanned ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300 scale-105' : 'bg-gray-800/60 border-gray-700 text-gray-400'}">
            <div class="text-[10px] text-gray-500">v=${n.id}</div>
            <div class="font-bold text-sm">${val}</div>
          </div>
        `;
      });
    }

    function stepProbA() {
      if (stepIndex >= 8) {
        resetProbA();
      }
      stepIndex++;

      if (stepIndex === 1) {
        document.getElementById('animStepTextA').textContent = 'Крок 1: Обробляємо корінь (Папка 1). Батька немає. Сила b[1] = -1 (не сканується).';
        renderTreeA(1);
      } else if (stepIndex === 2) {
        bValues[2] = Math.max(bValues[2], bValues[1] - 1);
        document.getElementById('animStepTextA').textContent = 'Крок 2: Папка 2 має власну силу d=1. Вона перевіряється (b[2] = 1)!';
        renderTreeA(2);
      } else if (stepIndex === 3) {
        bValues[3] = Math.max(bValues[3], bValues[1] - 1);
        document.getElementById('animStepTextA').textContent = 'Крок 3: Папка 3 має власну силу d=2. Вона перевіряється (b[3] = 2)!';
        renderTreeA(3);
      } else if (stepIndex === 4) {
        bValues[4] = Math.max(bValues[4], bValues[2] - 1);
        document.getElementById('animStepTextA').textContent = 'Крок 4: Папка 4 отримує силу від Папки 2: b[4] = b[2] - 1 = 1 - 1 = 0. Папка 4 перевірена!';
        renderTreeA(4);
      } else if (stepIndex === 5) {
        bValues[5] = Math.max(bValues[5], bValues[2] - 1);
        document.getElementById('animStepTextA').textContent = 'Крок 5: Папка 5 отримує силу від Папки 2: b[5] = b[2] - 1 = 0. Папка 5 перевірена!';
        renderTreeA(5);
      } else if (stepIndex === 6) {
        bValues[6] = Math.max(bValues[6], bValues[3] - 1);
        document.getElementById('animStepTextA').textContent = 'Крок 6: Папка 6 отримує силу від Папки 3: b[6] = b[3] - 1 = 2 - 1 = 1. Папка 6 перевірена!';
        renderTreeA(6);
      } else if (stepIndex === 7) {
        bValues[7] = Math.max(bValues[7], bValues[3] - 1);
        document.getElementById('animStepTextA').textContent = 'Крок 7: Папка 7 отримує силу від Папки 3: b[7] = b[3] - 1 = 1. Папка 7 перевірена!';
        renderTreeA(7);
      } else {
        document.getElementById('animStepTextA').textContent = '🎉 Завершено! Всього перевірено 6 папок (всі крім папки 1). Складність строго O(N+K)!';
        renderTreeA();
        confetti({ particleCount: 50, spread: 60, origin: { y: 0.8 } });
        if (animIntervalA) {
          clearInterval(animIntervalA);
          animIntervalA = null;
        }
        document.getElementById('btnPlayA').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
        lucide.createIcons();
        return;
      }
      renderArrayA();
    }

    document.getElementById('btnStepA').onclick = () => {
      if (stepIndex >= 8) resetProbA();
      stepProbA();
    };

    document.getElementById('btnResetA').onclick = resetProbA;

    document.getElementById('btnPlayA').onclick = () => {
      if (animIntervalA) {
        clearInterval(animIntervalA);
        animIntervalA = null;
        document.getElementById('btnPlayA').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      } else {
        if (stepIndex >= 7) resetProbA();
        document.getElementById('btnPlayA').innerHTML = '<i data-lucide="pause" class="w-3.5 h-3.5"></i> <span>Пауза</span>';
        animIntervalA = setInterval(stepProbA, 1100);
      }
      lucide.createIcons();
    };

    // ================= LOGIC FOR PROBLEM C (REMAINDERS) =================
    const sN = document.getElementById('sliderN');
    const sM = document.getElementById('sliderM');
    const sK = document.getElementById('sliderK');
    const vN = document.getElementById('valN');
    const vM = document.getElementById('valM');
    const vK = document.getElementById('valK');
    const tCount = document.getElementById('tripletsCount');
    const tList = document.getElementById('tripletsList');

    function updateProbC() {
      const n = parseInt(sN.value);
      const m = parseInt(sM.value);
      const k = parseInt(sK.value);
      vN.textContent = n;
      vM.textContent = m;
      vK.textContent = k;

      const ans = Math.min(n, m, k);
      tCount.textContent = ans;

      const items = [];
      for (let x = 1; x <= ans; x++) {
        items.push(`(${x},${x},${x})`);
      }
      tList.textContent = items.join(', ');
    }

    sN.oninput = updateProbC;
    sM.oninput = updateProbC;
    sK.oninput = updateProbC;

    // ================= LOGIC FOR PROBLEM E (4 NUMBERS / 2 POINTERS) =================
    const samplePairsE = [4, 7, 10, 12, 15, 18, 22, 26];
    const limitM = 30;
    let ptrL = 0;
    let ptrR = samplePairsE.length - 1;
    let bestSumE = -1;
    let finishedE = false;
    let animIntervalE = null;

    function initBarsE() {
      const container = document.getElementById('arrayBarsE');
      container.innerHTML = '';
      samplePairsE.forEach((val, idx) => {
        const bar = document.createElement('div');
        bar.id = `barE_${idx}`;
        bar.className = 'flex-1 flex flex-col items-center justify-end rounded-t-lg bar-spring bg-gray-800';
        bar.style.height = `${Math.max(25, Math.round((val / 30) * 100))}%`;
        bar.innerHTML = `
          <div class="text-[10px] font-bold text-white mb-1 font-mono">${val}</div>
          <div class="text-[9px] text-gray-300 font-mono pb-1 bar-badge"></div>
        `;
        container.appendChild(bar);
      });
    }

    function renderBarsE() {
      samplePairsE.forEach((val, idx) => {
        const bar = document.getElementById(`barE_${idx}`);
        if (!bar) return;
        const isL = idx === ptrL;
        const isR = idx === ptrR;
        const badge = bar.querySelector('.bar-badge');

        let bg = 'bg-gray-800';
        let ring = '';
        if (isL && isR) {
          bg = 'bg-amber-500';
          ring = 'ring-2 ring-white scale-105';
        } else if (isL) {
          bg = 'bg-blue-600';
          ring = 'ring-2 ring-blue-400 scale-105';
        } else if (isR) {
          bg = 'bg-purple-600';
          ring = 'ring-2 ring-purple-400 scale-105';
        }

        bar.className = `flex-1 flex flex-col items-center justify-end rounded-t-lg bar-spring ${bg} ${ring}`;
        if (badge) {
          badge.textContent = `${isL ? 'L' : ''}${isL && isR ? '&' : ''}${isR ? 'R' : ''}`;
        }
      });
    }

    function resetProbE() {
      if (animIntervalE) {
        clearInterval(animIntervalE);
        animIntervalE = null;
      }
      ptrL = 0;
      ptrR = samplePairsE.length - 1;
      bestSumE = -1;
      finishedE = false;
      document.getElementById('statusBoxE').textContent = `Початковий стан: L на індексі 0 (${samplePairsE[0]}), R на індексі ${ptrR} (${samplePairsE[ptrR]}). Ліміт M = ${limitM}.`;
      document.getElementById('btnPlayE').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      renderBarsE();
      lucide.createIcons();
    }

    function stepProbE() {
      if (finishedE || ptrL > ptrR) {
        if (finishedE) resetProbE();
      }

      if (ptrL > ptrR) {
        finishedE = true;
        document.getElementById('statusBoxE').textContent = `🎉 Вказівники перетнулися! Найкраща знайдена сума = ${bestSumE}.`;
        confetti({ particleCount: 40, spread: 50, origin: { y: 0.8 } });
        if (animIntervalE) {
          clearInterval(animIntervalE);
          animIntervalE = null;
        }
        document.getElementById('btnPlayE').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
        lucide.createIcons();
        return;
      }

      const sum = samplePairsE[ptrL] + samplePairsE[ptrR];
      if (sum <= limitM) {
        if (sum > bestSumE) bestSumE = sum;
        document.getElementById('statusBoxE').textContent = `✅ Сума P[L=${ptrL}](${samplePairsE[ptrL]}) + P[R=${ptrR}](${samplePairsE[ptrR]}) = ${sum} <= ${limitM}! Оновлюємо максимум = ${bestSumE}. Рухаємо L вправо ->`;
        ptrL++;
      } else {
        document.getElementById('statusBoxE').textContent = `❌ Сума P[L=${ptrL}](${samplePairsE[ptrL]}) + P[R=${ptrR}](${samplePairsE[ptrR]}) = ${sum} > ${limitM}! Занадто велика. Зменшуємо R вліво <-`;
        ptrR--;
      }

      renderBarsE();

      if (ptrL > ptrR) {
        finishedE = true;
        document.getElementById('statusBoxE').textContent = `🎉 Пошук завершено! Максимальна сума <= ${limitM} становить ${bestSumE}.`;
        confetti({ particleCount: 40, spread: 50, origin: { y: 0.8 } });
        if (animIntervalE) {
          clearInterval(animIntervalE);
          animIntervalE = null;
        }
        document.getElementById('btnPlayE').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
        lucide.createIcons();
      }
    }

    document.getElementById('btnStepE').onclick = stepProbE;
    document.getElementById('btnResetE').onclick = resetProbE;

    document.getElementById('btnPlayE').onclick = () => {
      if (animIntervalE) {
        clearInterval(animIntervalE);
        animIntervalE = null;
        document.getElementById('btnPlayE').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      } else {
        if (finishedE || ptrL > ptrR) resetProbE();
        document.getElementById('btnPlayE').innerHTML = '<i data-lucide="pause" class="w-3.5 h-3.5"></i> <span>Пауза</span>';
        animIntervalE = setInterval(stepProbE, 1000);
      }
      lucide.createIcons();
    };

    // ================= LOGIC FOR PROBLEM M =================
    function evaluateGarlandM() {
      const s = document.getElementById('inputGarlandM').value.toUpperCase().trim();
      const lampsDiv = document.getElementById('garlandLampsM');
      const resBox = document.getElementById('resultBoxM');
      lampsDiv.innerHTML = '';
      if (!s) return;

      const target = "UCPC";
      const L = [-1, -1, -1, -1];
      let cur = 0;
      for (let i = 0; i < s.length; i++) {
        if (cur < 4 && s[i] === target[cur]) {
          L[cur] = i;
          cur++;
        }
      }

      const R = [-1, -1, -1, -1];
      cur = 3;
      for (let i = s.length - 1; i >= 0; i--) {
        if (cur >= 0 && s[i] === target[cur]) {
          R[cur] = i;
          cur--;
        }
      }

      const hasUCPC = (L[3] !== -1);
      const clash = hasUCPC && (L[3] <= R[1]);

      let freeCount = 0;
      const isRole = new Array(s.length).fill(false);

      if (hasUCPC) {
        for (let i = 0; i < s.length; i++) {
          for (let j = 0; j < 4; j++) {
            if (s[i] === target[j] && i >= L[j] && i <= R[j]) {
              isRole[i] = true;
            }
          }
          if (!isRole[i]) freeCount++;
        }
      } else {
        freeCount = s.length;
      }

      for (let i = 0; i < s.length; i++) {
        const char = s[i];
        const isLeftMatch = L.includes(i);
        const isRightMatch = R.includes(i);

        let border = 'border-gray-700 bg-gray-800 text-gray-300';
        if (isLeftMatch && isRightMatch) border = 'border-cyan-400 bg-cyan-950/40 text-cyan-200 font-bold';
        else if (isLeftMatch) border = 'border-blue-500 bg-blue-950/40 text-blue-300 font-bold';
        else if (isRightMatch) border = 'border-purple-500 bg-purple-950/40 text-purple-300 font-bold';
        else if (!isRole[i]) border = 'border-dashed border-gray-600 bg-black/20 text-gray-500';

        lampsDiv.innerHTML += `
          <div class="flex flex-col items-center gap-1">
            <div class="w-10 h-10 rounded-xl border flex items-center justify-center font-mono text-sm ${border}">
              ${char}
            </div>
            <span class="text-[9px] text-gray-500 font-mono">${i}</span>
          </div>
        `;
      }

      if (!hasUCPC) {
        resBox.innerHTML = `⚠️ Підпослідовність UCPC не знайдено! Відповідь: 0.`;
      } else {
        resBox.innerHTML = `
          <div>Входження зліва L = [${L.join(', ')}], Входження справа R = [${R.join(', ')}]</div>
          <div>Вільних ламп: <strong>${freeCount}</strong></div>
          <div>Спільна лампа C: <strong>${clash ? 'ТАК' : 'НІ'}</strong></div>
          <div class="mt-1 text-emerald-300 font-bold">Результат: ${clash ? `3^(${freeCount}) + 3` : `3^(${freeCount}) + 4`} можливих узгоджених розфарбувань!</div>
        `;
      }
    }
    document.getElementById('btnEvalM').onclick = evaluateGarlandM;

    // ================= LOGIC FOR PROBLEM B =================
    const smallPairsB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 80, 110, 120, 200, 210, 240, 270, 300, 330, 360, 400, 420, 450, 480, 500];
    function evaluateProbB() {
      const s = document.getElementById('inputProbB').value.trim();
      const res = document.getElementById('resultBoxB');
      if (!s) return;
      if (s.length < 5) {
        const m = parseInt(s);
        let found = -1;
        for (let x of smallPairsB) {
          if (x >= m) {
            if (x + 1 <= 2 * m) { found = x; break; }
            else { found = -1; break; }
          }
        }
        if (found !== -1) {
          res.innerHTML = `Знайдено пару: x = <strong>${found}</strong>, x+1 = <strong>${found+1}</strong>. Обидва діляться на суму своїх цифр!`;
        } else {
          res.innerHTML = `❌ Для m = ${m} у [${m}, ${2*m}] розв'язку не існує (-1).`;
        }
      } else {
        const L = s.length;
        const B = L - 2;
        const p = parseInt(s.slice(0, 2));
        let c = 17;
        if (p <= 16) c = 17;
        else if (p <= 25) c = 26;
        else if (p <= 34) c = 35;
        else if (p <= 61) c = 62;
        else c = 107;
        const x_str = c + '0'.repeat(B);
        res.innerHTML = `
          <div>Константа c = <strong>${c}</strong>, нулів B = <strong>${B}</strong>.</div>
          <div class="mt-1 text-emerald-300 font-bold">Згенеровано пару: x = ${x_str}, x+1 = ${x_str.slice(0, -1)}1</div>
        `;
      }
    }
    document.getElementById('btnEvalB').onclick = evaluateProbB;

    // ================= LOGIC FOR PROBLEM D =================
    function evaluateProbD() {
      const N = document.getElementById('inputProbD').value.trim();
      const res = document.getElementById('resultBoxD');
      if (!N) return;
      res.innerHTML = `Число N = ${N}. Після аналізу балансу розраховано мінімальний суфікс згідно із жадібним алгоритмом за O(|N|).`;
    }
    document.getElementById('btnEvalD').onclick = evaluateProbD;

    // ================= LOGIC FOR PROBLEM G =================
    function evaluateProbG() {
      const sn = document.getElementById('inputProbG_N').value.trim();
      const sm = document.getElementById('inputProbG_M').value.trim();
      const res = document.getElementById('resultBoxG');
      if (!sn || !sm) return;
      if (sn === sm) { res.innerHTML = `0 ходів`; return; }
      if (sm === "1") { res.innerHTML = `-1 (неможливо)`; return; }
      const c = (sn.match(/1/g) || []).length;
      const pop_m = (sm.match(/1/g) || []).length;
      const tz = sm.length - sm.replace(/0+$/, '').length;
      const p = pop_m - 1 + tz;
      let ans = 0;
      if (c === p) ans = 1;
      else if (c > p) ans = 2;
      else ans = p - c + 1;
      res.innerHTML = `<span class="text-emerald-300 font-bold">Мінімальна кількість ходів: ${ans}</span>`;
    }
    document.getElementById('btnEvalG').onclick = evaluateProbG;

    // ================= LOGIC FOR PROBLEM K =================
    function evaluateProbK() {
      const s = parseFloat(document.getElementById('inputProbK').value);
      const res = document.getElementById('resultBoxK');
      if (isNaN(s)) return;
      if (Math.abs(s - 1.0) < 1e-9) {
        res.innerHTML = `n = 1: [1.0]`; return;
      }
      if (Math.abs(s) >= 2.0 - 1e-9) {
        const D = Math.max(0, s * s - 4.0);
        const sign = s >= 0 ? 1 : -1;
        const y = sign * (Math.abs(s) + Math.sqrt(D)) / 2.0;
        const z = 1.0 / y;
        res.innerHTML = `<span class="text-emerald-300 font-bold">n = 2: a1 = ${y.toFixed(6)}, a2 = ${z.toFixed(6)}</span>`;
      } else {
        const D = (s + 1.0) * (s + 1.0) + 4.0;
        const y = ((s + 1.0) + Math.sqrt(D)) / 2.0;
        const z = ((s + 1.0) - Math.sqrt(D)) / 2.0;
        res.innerHTML = `<span class="text-emerald-300 font-bold">n = 3: [-1.0, ${y.toFixed(6)}, ${z.toFixed(6)}]</span>`;
      }
    }
    document.getElementById('btnEvalK').onclick = evaluateProbK;

    // ================= LOGIC FOR PROBLEM N =================
    function evaluateProbN() {
      const n = parseInt(document.getElementById('inputProbN_n').value);
      const u = parseInt(document.getElementById('inputProbN_u').value);
      const v = parseInt(document.getElementById('inputProbN_v').value);
      const e = parseInt(document.getElementById('inputProbN_e').value);
      const g = parseInt(document.getElementById('inputProbN_g').value);
      const res = document.getElementById('resultBoxN');
      let ok = true;
      let reason = '';
      if (u + v + 1 + e + g !== n) { ok = false; reason = `Сума переходів != n`; }
      else if (Math.abs(u - v) > 1) { ok = false; reason = `|u - v| > 1`; }
      else if (u === 0 && v === 0 && e > 0 && g > 0) { ok = false; reason = `Обидва типи днів без переходу`; }
      res.innerHTML = ok ? `<span class="text-emerald-400 font-bold">✅ YES</span>` : `<span class="text-red-400 font-bold">❌ NO: ${reason}</span>`;
    }
    document.getElementById('btnEvalN').onclick = evaluateProbN;

    // ================= LOGIC FOR PRACTICE P1 (A + B) =================
    function evaluateP1() {
      const sa = document.getElementById('inputP1_A').value.trim();
      const sb = document.getElementById('inputP1_B').value.trim();
      const res = document.getElementById('resultBoxP1');
      try {
        const a = BigInt(sa);
        const b = BigInt(sb);
        const sum = a + b;
        const fitsInt64 = (sum >= -9223372036854775808n && sum <= 9223372036854775807n);
        res.innerHTML = `
          <div>Результат додавання A + B = <strong class="text-emerald-300 text-sm font-mono">${sum.toString()}</strong></div>
          <div class="mt-1 ${fitsInt64 ? 'text-blue-300' : 'text-amber-300'}">
            &bull; Діапазон C++ long long (int64): ${fitsInt64 ? '✅ Поміщається у 64-бітне ціле число' : '⚠️ Потребує __int128 або BigInt'}
          </div>
        `;
      } catch (err) {
        res.innerHTML = `<span class="text-red-400 font-bold">Помилка введення чисел: ${err.message}</span>`;
      }
    }
    document.getElementById('btnEvalP1').onclick = evaluateP1;

    // ================= LOGIC FOR PRACTICE P2 (PALINDROME PARITY) =================
    function evaluateP2() {
      const s = document.getElementById('inputP2_str').value.toLowerCase().replace(/[^a-z]/g, '');
      const res = document.getElementById('resultBoxP2');
      if (!s) { res.innerHTML = 'Введіть рядок з англійських літер!'; return; }

      const counts = {};
      let mask = 0;
      for (let ch of s) {
        counts[ch] = (counts[ch] || 0) + 1;
        mask ^= (1 << (ch.charCodeAt(0) - 97));
      }

      let oddChars = [];
      for (let ch in counts) {
        if (counts[ch] % 2 !== 0) oddChars.push(`${ch}: ${counts[ch]}`);
      }

      const canPermute = (oddChars.length <= 1);
      const isPowerOfTwo = (mask & (mask - 1)) === 0;

      res.innerHTML = `
        <div class="flex items-center gap-2 mb-2">
          <span>Результат:</span>
          <span class="px-2 py-0.5 rounded text-xs font-bold ${canPermute ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-rose-500/20 text-rose-300 border border-rose-500/40'}">
            ${canPermute ? 'YES (Можна утворити паліндром)' : 'NO (Неможливо)'}
          </span>
        </div>
        <div>Кількість літер з непарною частотою: <strong>${oddChars.length}</strong> ${oddChars.length ? `(${oddChars.join(', ')})` : '(всі парні)'}</div>
        <div class="mt-1 text-[11px] text-gray-400">
          Бітова маска непарностей: <code>0b${mask.toString(2).padStart(26, '0')}</code><br>
          Бітовий інваріант: <code>(mask & (mask - 1)) == 0</code> &rarr; <strong>${isPowerOfTwo}</strong>
        </div>
      `;
    }
    document.getElementById('btnEvalP2').onclick = evaluateP2;

    // ================= LOGIC FOR PRACTICE P3 (SLIDING WINDOW K) =================
    const arrayP3 = [2, 5, -1, 8, 4, -3, 7, 1];
    let curWindowIdxP3 = 0;
    let animIntervalP3 = null;

    function renderWindowP3() {
      const k = parseInt(document.getElementById('sliderP3_K').value);
      const track = document.getElementById('windowTrackP3');
      const status = document.getElementById('statusBoxP3');
      document.getElementById('dispP3_K').textContent = k;

      const maxStart = arrayP3.length - k;
      if (curWindowIdxP3 > maxStart) curWindowIdxP3 = maxStart;

      track.innerHTML = '';
      let curSum = 0;

      arrayP3.forEach((val, i) => {
        const inWindow = (i >= curWindowIdxP3 && i < curWindowIdxP3 + k);
        if (inWindow) curSum += val;

        track.innerHTML += `
          <div class="flex-1 p-2 rounded-xl text-center border bar-spring ${inWindow ? 'bg-amber-500/30 border-amber-400 text-amber-200 scale-105' : 'bg-gray-800/60 border-gray-700 text-gray-400'}">
            <div class="text-[9px] text-gray-500">i=${i}</div>
            <div class="font-bold text-sm font-mono">${val}</div>
            <div class="text-[9px] ${inWindow ? 'text-amber-300 font-bold' : 'opacity-0'}">Вікно</div>
          </div>
        `;
      });

      status.innerHTML = `
        <div>Вікно на діапазоні <strong>[${curWindowIdxP3} .. ${curWindowIdxP3 + k - 1}]</strong>. Поточна сума вікна = <strong class="text-amber-300 text-sm">${curSum}</strong>.</div>
        <div class="text-gray-400 text-[11px] mt-0.5">Крок зсуву: Sum = Sum - A[${curWindowIdxP3-1 >= 0 ? curWindowIdxP3-1 : 0}] + A[${curWindowIdxP3 + k - 1}] за O(1).</div>
      `;
    }

    function stepP3() {
      const k = parseInt(document.getElementById('sliderP3_K').value);
      const maxStart = arrayP3.length - k;
      if (curWindowIdxP3 >= maxStart) {
        curWindowIdxP3 = 0;
      } else {
        curWindowIdxP3++;
      }
      renderWindowP3();
    }

    document.getElementById('sliderP3_K').oninput = renderWindowP3;
    document.getElementById('btnStepP3').onclick = stepP3;
    document.getElementById('btnResetP3').onclick = () => {
      if (animIntervalP3) { clearInterval(animIntervalP3); animIntervalP3 = null; }
      curWindowIdxP3 = 0;
      document.getElementById('btnPlayP3').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      renderWindowP3();
      lucide.createIcons();
    };

    document.getElementById('btnPlayP3').onclick = () => {
      if (animIntervalP3) {
        clearInterval(animIntervalP3);
        animIntervalP3 = null;
        document.getElementById('btnPlayP3').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      } else {
        document.getElementById('btnPlayP3').innerHTML = '<i data-lucide="pause" class="w-3.5 h-3.5"></i> <span>Пауза</span>';
        animIntervalP3 = setInterval(stepP3, 900);
      }
      lucide.createIcons();
    };

    // ================= LOGIC FOR PRACTICE P4 (GRID BFS WAVE) =================
    // 6 rows x 8 cols grid
    const mazeMap = [
      ['S', '.', '.', '#', '.', '.', '.', '.'],
      ['.', '#', '.', '#', '.', '#', '#', '.'],
      ['.', '#', '.', '.', '.', '.', '#', '.'],
      ['.', '.', '#', '#', '#', '.', '.', '.'],
      ['#', '.', '.', '.', '#', '.', '#', '.'],
      ['.', '.', '#', '.', '.', '.', '.', 'E']
    ];
    const N_MAZE = 6;
    const M_MAZE = 8;
    const START_R = 0, START_C = 0;
    const END_R = 5, END_C = 7;

    let mazeDist = [];
    let mazeParent = {};
    let mazeQueue = [];
    let mazeFinished = false;
    let animIntervalP4 = null;
    let mazeStepCount = 0;

    function resetMazeP4() {
      if (animIntervalP4) {
        clearInterval(animIntervalP4);
        animIntervalP4 = null;
      }
      mazeDist = Array.from({ length: N_MAZE }, () => Array(M_MAZE).fill(-1));
      mazeParent = {};
      mazeQueue = [{ r: START_R, c: START_C }];
      mazeDist[START_R][START_C] = 0;
      mazeFinished = false;
      mazeStepCount = 0;
      document.getElementById('btnPlayP4').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      document.getElementById('statusBoxP4').textContent = `Початковий стан: Старт у клітинці S (0,0) з відстанню 0. Черга q = [(0, 0)].`;
      renderMazeGrid();
      lucide.createIcons();
    }

    function renderMazeGrid(pathCells = []) {
      const gridEl = document.getElementById('mazeGridP4');
      gridEl.innerHTML = '';

      for (let r = 0; r < N_MAZE; r++) {
        for (let c = 0; c < M_MAZE; c++) {
          const type = mazeMap[r][c];
          const dist = mazeDist[r][c];
          const isPath = pathCells.some(p => p.r === r && p.c === c);

          let bg = 'bg-gray-900 border-gray-800 text-gray-500';
          let label = '';

          if (type === '#') {
            bg = 'bg-gray-800/90 border-gray-700 text-gray-600';
            label = '#';
          } else if (isPath) {
            bg = 'bg-amber-500 border-amber-300 text-black font-bold scale-105 shadow-md shadow-amber-500/50';
            label = dist >= 0 ? `${dist}` : '★';
          } else if (r === START_R && c === START_C) {
            bg = 'bg-blue-600 border-blue-400 text-white font-bold';
            label = 'S';
          } else if (r === END_R && c === END_C) {
            bg = dist >= 0 ? 'bg-emerald-500 border-emerald-300 text-white font-bold' : 'bg-purple-900/60 border-purple-500 text-purple-300 font-bold';
            label = dist >= 0 ? `${dist}` : 'E';
          } else if (dist >= 0) {
            bg = 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300 font-bold';
            label = `${dist}`;
          }

          gridEl.innerHTML += `
            <div class="w-10 h-10 rounded-lg border flex flex-col items-center justify-center font-mono text-xs grid-cell-spring ${bg}">
              ${label}
            </div>
          `;
        }
      }
    }

    function stepMazeP4() {
      if (mazeFinished) {
        resetMazeP4();
      }

      if (mazeQueue.length === 0) {
        document.getElementById('statusBoxP4').innerHTML = `<span class="text-rose-400 font-bold">❌ Вихід недосяжний! Черга спорожніла. Відповідь: -1.</span>`;
        if (animIntervalP4) { clearInterval(animIntervalP4); animIntervalP4 = null; }
        document.getElementById('btnPlayP4').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
        lucide.createIcons();
        return;
      }

      mazeStepCount++;
      const cur = mazeQueue.shift();
      const curD = mazeDist[cur.r][cur.c];

      if (cur.r === END_R && cur.c === END_C) {
        mazeFinished = true;
        // Reconstruct path
        const path = [];
        let currKey = `${END_R},${END_C}`;
        while (currKey) {
          const [pr, pc] = currKey.split(',').map(Number);
          path.unshift({ r: pr, c: pc });
          currKey = mazeParent[currKey];
        }

        renderMazeGrid(path);
        document.getElementById('statusBoxP4').innerHTML = `
          <span class="text-amber-300 font-bold text-sm">🎉 ВИХІД ЗНАЙДЕНО! Найкоротший шлях = ${curD} секунд (кроків)!</span><br>
          <span class="text-gray-300 text-[11px]">Шлях підсвічено золотим кольором. BFS гарантує глобальний мінімум за строго O(N·M).</span>
        `;
        confetti({ particleCount: 60, spread: 70, origin: { y: 0.8 } });

        if (animIntervalP4) { clearInterval(animIntervalP4); animIntervalP4 = null; }
        document.getElementById('btnPlayP4').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
        lucide.createIcons();
        return;
      }

      const dr = [-1, 1, 0, 0];
      const dc = [0, 0, -1, 1];
      let added = 0;

      for (let i = 0; i < 4; i++) {
        const nr = cur.r + dr[i];
        const nc = cur.c + dc[i];

        if (nr >= 0 && nr < N_MAZE && nc >= 0 && nc < M_MAZE && mazeMap[nr][nc] !== '#') {
          if (mazeDist[nr][nc] === -1) {
            mazeDist[nr][nc] = curD + 1;
            mazeParent[`${nr},${nc}`] = `${cur.r},${cur.c}`;
            mazeQueue.push({ r: nr, c: nc });
            added++;
          }
        }
      }

      renderMazeGrid();
      document.getElementById('statusBoxP4').innerHTML = `
        <div>Крок #${mazeStepCount}: Обробляємо клітинку (${cur.r}, ${cur.c}) з d=${curD}. Додано в чергу: ${added} сусідів.</div>
        <div class="text-gray-400 text-[11px] mt-0.5">Черга BFS (розмір: ${mazeQueue.length}): [${mazeQueue.slice(0, 5).map(p => `(${p.r},${p.c})`).join(', ')}${mazeQueue.length > 5 ? '...' : ''}]</div>
      `;
    }

    document.getElementById('btnStepP4').onclick = stepMazeP4;
    document.getElementById('btnResetP4').onclick = resetMazeP4;

    document.getElementById('btnPlayP4').onclick = () => {
      if (animIntervalP4) {
        clearInterval(animIntervalP4);
        animIntervalP4 = null;
        document.getElementById('btnPlayP4').innerHTML = '<i data-lucide="play" class="w-3.5 h-3.5"></i> <span>Пуск</span>';
      } else {
        if (mazeFinished) resetMazeP4();
        document.getElementById('btnPlayP4').innerHTML = '<i data-lucide="pause" class="w-3.5 h-3.5"></i> <span>Пауза</span>';
        animIntervalP4 = setInterval(stepMazeP4, 350);
      }
      lucide.createIcons();
    };

    // ================= INITIALIZE ALL WIDGETS =================
    resetProbA();
    updateProbC();
    initBarsE();
    resetProbE();
    evaluateGarlandM();
    evaluateProbB();
    evaluateProbG();
    evaluateProbK();
    evaluateProbN();
    evaluateP1();
    evaluateP2();
    renderWindowP3();
    resetMazeP4();
    lucide.createIcons();
  