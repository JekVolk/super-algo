
    // 5-LEVEL ULTRA DECOMPOSITION KNOWLEDGE BASE
    const KNOWLEDGE_TREE = [
      {
        macro_id: 'macro_dp',
        macro_title: '1. Динамічне Програмування (Dynamic Programming Mastery)',
        description: 'Оптимізаційні задачі з властивістю оптимальної підструктури та перекриттям підзадач.',
        topics: [
          {
            topic_id: 'dp_bitmask',
            topic_title: 'ДП по бітових масках (Bitmask DP)',
            subtopics: [
              {
                subtopic_id: 'dp_bitmask_subsets',
                subtopic_title: 'Перебір підмасок маски (Iterating Submasks)',
                microtopics: [
                  {
                    micro_id: 'micro_submask_enumeration',
                    micro_title: 'Класичний цикл перебору підмасок за O(3^N)',
                    nanotopics: [
                      {
                        nano_id: 'nano_submask_idiom',
                        nano_title: 'Ідіома s = (s - 1) & mask',
                        summary: 'Дозволяє перебрати всі 2^k підмасок за O(1) на підмаску без зайвих перевірок.',
                        invariant: 'Кожен біт, який не встановлений у mask, завжди обнуляється операцією & mask.',
                        contest_trap: 'Зациклення при досягненні s == 0, якщо умова циклу s >= 0 (потрібно for(int s = mask; s; s = (s - 1) & mask) та окремо s = 0).',
                        code_snippet: 'for (int s = mask; s > 0; s = (s - 1) & mask) {\n    // обробка підмаски s\n}\n// обробити s = 0 окремо!'
                      },
                      {
                        nano_id: 'nano_sos_dp',
                        nano_title: 'Sum over Subsets (SOS DP) за O(N · 2^N)',
                        summary: 'Динаміка по бітах замість O(3^N) для обчислення сум по всіх підмасках.',
                        invariant: 'dp[i][mask] містить суму значень для підмасок, що відрізняються від mask лише у перших i бітах.',
                        contest_trap: 'Переплутаний порядок циклів: зовнішній цикл повинен іти по номеру біта (0..N-1), а внутрішній по масці (0..2^N-1).',
                        code_snippet: 'for (int i = 0; i < N; ++i) {\n    for (int mask = 0; mask < (1 << N); ++mask) {\n        if (mask & (1 << i)) dp[mask] += dp[mask ^ (1 << i)];\n    }\n}'
                      }
                    ]
                  }
                ]
              },
              {
                subtopic_id: 'dp_tsp_matching',
                subtopic_title: 'Задача комівояжера (TSP) та мінімальне паросполучення',
                microtopics: [
                  {
                    micro_id: 'micro_tsp_states',
                    micro_title: 'Стан dp[mask][last_v] для пошуку гамільтонового шляху',
                    nanotopics: [
                      {
                        nano_id: 'nano_tsp_base_case',
                        nano_title: 'Базовий випадок і початкова ініціалізація нескінченністю',
                        summary: 'Ініціалізація dp[1 << start][start] = 0, решта INF (0x3f3f3f3f), щоб уникнути переповнення при додаванні ребра.',
                        invariant: 'Будь-який стан з n бітами переходить тільки у стан з n+1 бітами (гарантує DAG без циклів).',
                        contest_trap: 'Використання 0x7fffffff (INT_MAX), що викликає int32 overflow при dp + cost.',
                        code_snippet: 'memset(dp, 0x3f, sizeof(dp));\ndp[1 << 0][0] = 0;'
                      },
                      {
                        nano_id: 'nano_matching_canonical',
                        nano_title: 'Канонічний вибір першого вільного біта __builtin_ctz(~mask)',
                        summary: 'Зниження складності паросполучення з O(N^2 · 2^N) до O(N · 2^N) через фіксацію найменшого вільного елемента.',
                        invariant: 'Порядок парування не має значення, тому перший невикористаний елемент зобов\'язаний з кимось спаруватися.',
                        contest_trap: 'Подвійний підрахунок пар (комбінаторний вибух), якщо не фіксувати перший елемент.',
                        code_snippet: 'int first_free = __builtin_ctz((~mask) & ((1 << N) - 1));'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'dp_tree',
            topic_title: 'ДП на деревах (Tree DP)',
            subtopics: [
              {
                subtopic_id: 'dp_tree_rerooting',
                subtopic_title: 'Техніка перепідвішування кореня (Rerooting / All Roots DP)',
                microtopics: [
                  {
                    micro_id: 'micro_rerooting_two_dfs',
                    micro_title: 'Двопрохідний DFS з префіксними та суфіксними префіксами',
                    nanotopics: [
                      {
                        nano_id: 'nano_prefix_suffix_tree_exclusion',
                        nano_title: 'Виключення внеску сина через масиви pref/suff',
                        summary: 'Коли операція злиття не має зворотної (напр. std::max), внесок v виключається через префіксні і суфіксні максимуми братів.',
                        invariant: 'Сукупний внесок усіх дітей крім v дорівнює pref[i-1] ⊕ suff[i+1].',
                        contest_trap: 'Спроба ділити або віднімати за наявності нулів або незворотних напівкілець (max/min/gcd).',
                        code_snippet: '// pref_dp[i] = combine(pref_dp[i-1], child[i])\n// suff_dp[i] = combine(suff_dp[i+1], child[i])'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'dp_optimizations',
            topic_title: 'Олімпіадні Оптимізації ДП (DP Optimizations)',
            subtopics: [
              {
                subtopic_id: 'dp_cht',
                subtopic_title: 'Convex Hull Trick (CHT) та Li Chao Tree',
                microtopics: [
                  {
                    micro_id: 'micro_cht_static',
                    micro_title: 'Класичний CHT з монотонними кутовими коефіцієнтами k_i за O(N)',
                    nanotopics: [
                      {
                        nano_id: 'nano_cht_intersection_inequality',
                        nano_title: 'Умова видалення непотрібної прямої через перетин',
                        summary: 'Пряма L2 марна, якщо точка перетину intersect(L1, L3) лівіша за intersect(L1, L2).',
                        invariant: 'Кутові коефіцієнти прямих у двозв\'язній черзі строго зростають/спадають.',
                        contest_trap: 'Ділення з плаваючою крапкою double (втрата точності); слід використовувати множення (__int128).',
                        code_snippet: '// Перевірка: (b3 - b1) * (k1 - k2) <= (b2 - b1) * (k1 - k3)'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        macro_id: 'macro_ds',
        macro_title: '2. Просунуті Структури Даних (Advanced Data Structures)',
        description: 'Ефективне зберігання, модифікація та запити на підмножинах за логарифмічний час.',
        topics: [
          {
            topic_id: 'ds_segtree',
            topic_title: 'Дерево відрізків (Segment Tree)',
            subtopics: [
              {
                subtopic_id: 'ds_lazy_propagation',
                subtopic_title: 'Відкладені операції (Lazy Propagation)',
                microtopics: [
                  {
                    micro_id: 'micro_lazy_push_pull',
                    micro_title: 'Розділення обов\'язків push() та pull() (або combine())',
                    nanotopics: [
                      {
                        nano_id: 'nano_lazy_assignment_vs_addition',
                        nano_title: 'Сумісність операцій присвоєння (set) та додавання (add)',
                        summary: 'Присвоєння повністю анулює попереднє накопичене додавання у вузлі.',
                        invariant: 'Перед спуском у лівого і правого нащадків lazy-мітка батька зобов\'язана бути скинута у нуль (push).',
                        contest_trap: 'Забутий виклик push() у запиті query() при неповному покритті відрізка.',
                        code_snippet: 'void push(int v, int l, int r) {\n    if (!has_lazy[v]) return;\n    int mid = (l + r) / 2;\n    apply(2 * v, l, mid, lazy[v]);\n    apply(2 * v + 1, mid + 1, r, lazy[v]);\n    has_lazy[v] = false;\n}'
                      },
                      {
                        nano_id: 'nano_segtree_4n_bound',
                        nano_title: 'Правильний ліміт розміру дерева: 4 * N',
                        summary: 'Для довільного N дерево відрізків вимагає до 4N елементів через неповні нижні шари.',
                        invariant: 'Найближчий степінь двійки 2^{ceil(log2(N)) + 1} <= 4N.',
                        contest_trap: 'Виділення масиву розміром 2 * N призводить до непередбачуваного Runtime Error (SIGSEGV) на контесті.',
                        code_snippet: 'const int MAXN = 200000;\nint tree[4 * MAXN];\nint lazy[4 * MAXN];'
                      }
                    ]
                  }
                ]
              },
              {
                subtopic_id: 'ds_persistent_segtree',
                subtopic_title: 'Персистентне дерево відрізків (Persistent Segment Tree)',
                microtopics: [
                  {
                    micro_id: 'micro_kth_order_statistic',
                    micro_title: 'K-та порядкова статистика на відрізку [L, R] за O(log N)',
                    nanotopics: [
                      {
                        nano_id: 'nano_persistent_root_diff',
                        nano_title: 'Інваріант різниці коренів tree[root[R]].count - tree[root[L-1]].count',
                        summary: 'Відрізок [L, R] представляється як префіксний масив дерев: Root(R) мінус Root(L-1).',
                        invariant: 'Кількість елементів у діапазоні значень [val_l, val_r] дорівнює count(R) - count(L-1).',
                        contest_trap: 'Індексація L з одиниці: віднімання кореня root[L] замість root[L-1] виключає елемент на позиції L.',
                        code_snippet: 'int count_left = tree[tree[v_r].left].cnt - tree[tree[v_l].left].cnt;\nif (k <= count_left) query(tree[v_l].left, tree[v_r].left, l, mid, k);\nelse query(tree[v_l].right, tree[v_r].right, mid + 1, r, k - count_left);'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'ds_dsu',
            topic_title: 'Система неперетинних множин (Disjoint Set Union / DSU)',
            subtopics: [
              {
                subtopic_id: 'ds_dsu_rollback',
                subtopic_title: 'DSU з можливістю відкату (DSU with Rollback)',
                microtopics: [
                  {
                    micro_id: 'micro_dsu_stack_history',
                    micro_title: 'Історія змін у стеці без евристики стиснення шляху за O(log N)',
                    nanotopics: [
                      {
                        nano_id: 'nano_dsu_no_path_compression',
                        nano_title: 'Заборона стиснення шляху parent[x] = find(...) при відкатах',
                        summary: 'Стиснення шляху руйнує деревоподібну історію і робить точний відкат неможливим.',
                        invariant: 'Глибина дерева обмежена O(log N) завдяки строгій евристиці за розміром або рангом (union-by-rank).',
                        contest_trap: 'Автоматичне написання стиснення шляху, що ламає збережені у стеці попередні розміри.',
                        code_snippet: 'int find(int i) {\n    while (i != parent[i]) i = parent[i];\n    return i;\n}'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        macro_id: 'macro_graphs',
        macro_title: '3. Теорія Графів та Мереж (Graph & Network Theory)',
        description: 'Моделювання зв\'язків, найкоротших шляхів, мостів, потоків та паросполучень.',
        topics: [
          {
            topic_id: 'graphs_shortest_paths',
            topic_title: 'Найкоротші шляхи (Shortest Paths)',
            subtopics: [
              {
                subtopic_id: 'graphs_dijkstra',
                subtopic_title: 'Алгоритм Дейкстри',
                microtopics: [
                  {
                    micro_id: 'micro_dijkstra_pq',
                    micro_title: 'Оптимізація з std::priority_queue за O(M log N)',
                    nanotopics: [
                      {
                        nano_id: 'nano_dijkstra_stale_pair_check',
                        nano_title: 'Фільтрація застарілих пар: if (d > dist[u]) continue;',
                        summary: 'Черга з пріоритетом може містити до O(M) старих записів для однієї вершини.',
                        invariant: 'Коли вершина витягується з мінімальною вагою вперше, її шлях гарантовано фіналізований.',
                        contest_trap: 'Пропуск перевірки d > dist[u] спричиняє сповільнення до O(M log M) і TLE на щільних графах.',
                        code_snippet: 'auto [d, u] = pq.top(); pq.pop();\nif (d > dist[u]) continue;'
                      },
                      {
                        nano_id: 'nano_dijkstra_long_long',
                        nano_title: 'Зберігання відстаней у 64-бітному типі long long',
                        summary: 'Шлях з N-1 ребер довжиною до 10^9 перевищує 2^31 - 1 уже при N > 3.',
                        invariant: 'Максимальна відстань <= (N - 1) * MAX_W.',
                        contest_trap: 'Використання int для пари у priority_queue pair<int, int> викликає переповнення та нескінченний цикл.',
                        code_snippet: 'priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;'
                      }
                    ]
                  }
                ]
              },
              {
                subtopic_id: 'graphs_01bfs',
                subtopic_title: '0-1 BFS за O(V + E)',
                microtopics: [
                  {
                    micro_id: 'micro_01bfs_deque',
                    micro_title: 'Використання std::deque замість priority_queue',
                    nanotopics: [
                      {
                        nano_id: 'nano_deque_push_policy',
                        nano_title: 'Ребро 0 -> push_front(), Ребро 1 -> push_back()',
                        summary: 'Гарантує підтримку інваріанту монотонності відстаней у черзі без сортування.',
                        invariant: 'Різниця відстаней між головою та хвостом дека ніколи не перевищує 1.',
                        contest_trap: 'Помилковий push_back для ваги 0 руйнує порядок монотонності.',
                        code_snippet: 'if (w == 0) q.push_front(to);\nelse q.push_back(to);'
                      }
                    ]
                  }
                ]
              },
              {
                subtopic_id: 'graphs_grid_bfs',
                subtopic_title: 'BFS на сітці та Хвильовий спуск (Grid BFS & Tree Wave)',
                microtopics: [
                  {
                    micro_id: 'micro_grid_bfs_queue',
                    micro_title: 'Пошук найкоротшого шляху на сітці N x M (UCPC Practice Problem 4)',
                    nanotopics: [
                      {
                        nano_id: 'nano_visited_on_push',
                        nano_title: 'Пастка відвіданості: dist[nr][nc] = d + 1 строго ПЕРЕД q.push()',
                        summary: 'Позначення клітинки відвіданою при pop() замість push() роздуває чергу у 4 рази на кожному шарі і спричиняє жорсткий MLE/TLE.',
                        invariant: 'Черга зберігає монотонність відстаней (dist[tail] - dist[head] <= 1), кожна клітинка пушиться рівно 1 раз.',
                        contest_trap: 'Позначення відвіданості при вилученні (pop): клітинка потрапляє в чергу 4 рази від усіх сусідів.',
                        code_snippet: 'dist[nr][nc] = dist[r][c] + 1;\nq.push({nr, nc}); // Позначати ОДРАЗУ перед push!'
                      }
                    ]
                  },
                  {
                    micro_id: 'micro_tree_downward_wave',
                    micro_title: 'Хвильовий спуск по дереву папок за O(N + K) (UCPC Stage 1 Problem A)',
                    nanotopics: [
                      {
                        nano_id: 'nano_topological_array_pass',
                        nano_title: 'Інваріант a_v < v: прохід звичайним циклом for (v = 1..n)',
                        summary: 'Оскільки батько завжди має менший номер, ніж будь-який нащадок, дерево вже топологічно відсортоване.',
                        invariant: 'Коли цикл доходить до вершини v, залишок сили її батька a_v уже повністю обчислений.',
                        contest_trap: 'Рекурсивний DFS на бамбуковому дереві глибиною 200 000 спричиняє Stack Overflow (SIGSEGV).',
                        code_snippet: 'for (int v = 1; v <= n; ++v) {\n    if (a[v] > 0) b[v] = max(b[v], b[a[v]] - 1);\n}'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'graphs_connectivity',
            topic_title: 'Зв\'язність та Компоненти (Connectivity & Bridges)',
            subtopics: [
              {
                subtopic_id: 'graphs_tarjan_bridges',
                subtopic_title: 'Мости та точки зчленування (Tarjan\'s Bridges)',
                microtopics: [
                  {
                    micro_id: 'micro_tarjan_tin_low',
                    micro_title: 'Масиви часу входу tin[u] та мінімальної досяжності low[u]',
                    nanotopics: [
                      {
                        nano_id: 'nano_bridge_strict_inequality',
                        nano_title: 'Строга нерівність моста: low[to] > tin[u]',
                        summary: 'Ребро (u, to) є мостом тоді і тільки тоді, коли з піддерева to немає зворотних ребер у предків u.',
                        invariant: 'Для точок зчленування нерівність нестрога low[to] >= tin[u] (крім кореня DFS).',
                        contest_trap: 'Випадковий перехід по ребру назад до безпосереднього батька p (потрібно if (to == parent) continue).',
                        code_snippet: 'low[u] = min(low[u], low[to]);\nif (low[to] > tin[u]) {\n    // Ребро (u, to) — МІСТ!\n}'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        macro_id: 'macro_math',
        macro_title: '4. Олімпіадна Математика та Теорія Чисел',
        description: 'Теорія чисел, модулярна арифметика, комбінаторика, матриці та теорія ігор.',
        topics: [
          {
            topic_id: 'math_primes',
            topic_title: 'Прості числа та подільність (Primes & Factoring)',
            subtopics: [
              {
                subtopic_id: 'math_linear_sieve',
                subtopic_title: 'Лінійне решето Ератосфена за строго O(N)',
                microtopics: [
                  {
                    micro_id: 'micro_min_prime_factor',
                    micro_title: 'Кожне складене число викреслюється рівно один раз своїм найменшим простим дільником',
                    nanotopics: [
                      {
                        nano_id: 'nano_break_on_divisibility',
                        nano_title: 'Критична умова зупинки: if (i % p == 0) break;',
                        summary: 'Забезпечує лінійність O(N) замість O(N log log N).',
                        invariant: 'Для наступних простих p\' > p число i * p\' мало б дільник p, отже було б викреслено не своїм мінімальним дільником.',
                        contest_trap: 'Пропуск break повертає складність до звичайного решета з більшою константою.',
                        code_snippet: 'for (int p : primes) {\n    if (p > lp[i] || i * p > MAX) break;\n    lp[i * p] = p;\n    if (i % p == 0) break;\n}'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'math_combinatorics',
            topic_title: 'Комбінаторика за модулем MOD (10^9 + 7 / 998244353)',
            subtopics: [
              {
                subtopic_id: 'math_inverse_factorials',
                subtopic_title: 'Прекалькуляція факторіалів та зворотних факторіалів за O(N)',
                microtopics: [
                  {
                    micro_id: 'micro_single_mod_inv',
                    micro_title: 'Обчислення єдиного modInverse(fact[N]) і розмотування назад',
                    nanotopics: [
                      {
                        nano_id: 'nano_inv_fact_stepback',
                        nano_title: 'Крок назад: inv_fact[i-1] = (inv_fact[i] * i) % MOD',
                        summary: 'Усуває необхідність викликати розширений алгоритм Евкліда чи швидке піднесення N разів.',
                        invariant: '1 / (i - 1)! = i / i!.',
                        contest_trap: 'Виклик power(fact[i], MOD - 2) всередині циклу забирає O(N log MOD) і часто веде до TLE.',
                        code_snippet: 'inv_fact[N] = power(fact[N], MOD - 2);\nfor (int i = N; i >= 1; --i) {\n    inv_fact[i - 1] = (1LL * inv_fact[i] * i) % MOD;\n}'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        macro_id: 'macro_strings',
        macro_title: '5. Алгоритми на Рядках (Stringology)',
        description: 'Пошук зразків, аналіз періодичності, хешування, суфіксні та префіксні структури.',
        topics: [
          {
            topic_id: 'strings_hashing',
            topic_title: 'Поліноміальне Хешування (Rolling Hash)',
            subtopics: [
              {
                subtopic_id: 'strings_anti_hash_collision',
                subtopic_title: 'Захист від колізій та анти-хеш тестів',
                microtopics: [
                  {
                    micro_id: 'micro_double_random_hash',
                    micro_title: 'Подвійний хеш з рандомізованою базою',
                    nanotopics: [
                      {
                        nano_id: 'nano_random_base_chrono',
                        nano_title: 'Генерація бази через chrono::steady_clock',
                        summary: 'Фіксована база (наприклад, base = 31) вразлива до готових тестів-кілерів (Thue-Morse sequence) на Codeforces.',
                        invariant: 'Ймовірність колізії для пари модулів (10^9+7, 10^9+9) менше 10^{-18}.',
                        contest_trap: 'Використання unsigned long long з природним переповненням 2^64 (відомий анти-тест генератор взламує за O(N)).',
                        code_snippet: 'mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());\nconst int BASE = uniform_int_distribution<int>(300, 10000)(rng) | 1;'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        macro_id: 'macro_foundations',
        macro_title: '6. Алгоритмічні Основи, Пошук та Ad-Hoc',
        description: 'Базові шаблони мислення, робота з монотонністю та бітові маніпуляції.',
        topics: [
          {
            topic_id: 'foundations_binary_search',
            topic_title: 'Двійковий пошук (Binary Search)',
            subtopics: [
              {
                subtopic_id: 'bs_on_answer',
                subtopic_title: 'Бінарний пошук по відповіді (Bisection)',
                microtopics: [
                  {
                    micro_id: 'micro_bs_monotone_predicate',
                    micro_title: 'Предикат валідності check(mid) та інваріант меж',
                    nanotopics: [
                      {
                        nano_id: 'nano_bs_mid_overflow',
                        nano_title: 'Обчислення mid = low + (high - low) / 2',
                        summary: 'Унеможливлює переповнення при великих межах (наприклад, high = 2 * 10^9).',
                        invariant: 'Якщо check(mid) істинний, шукана відповідь належить [mid, high] (або [low, mid]).',
                        contest_trap: 'Зависання в нескінченному циклі при двох елементах high - low == 1, якщо ділення заокруглює не в той бік.',
                        code_snippet: 'long long low = 1, high = 2e18, ans = -1;\nwhile (low <= high) {\n    long long mid = low + (high - low) / 2;\n    if (check(mid)) { ans = mid; low = mid + 1; }\n    else { high = mid - 1; }\n}'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'foundations_bit_tricks',
            topic_title: 'Бітові операції та процесорні інструкції (Bitwise Hacks)',
            subtopics: [
              {
                subtopic_id: 'bit_builtins',
                subtopic_title: 'Вбудовані функції GCC (__builtin_*)',
                microtopics: [
                  {
                    micro_id: 'micro_fast_bit_math',
                    micro_title: 'Обчислення кількості бітів та позицій за 1 такт процесора',
                    nanotopics: [
                      {
                        nano_id: 'nano_builtin_64bit_suffix',
                        nano_title: 'Обов\'язковий суфікс ll: __builtin_popcountll(x)',
                        summary: 'Для чисел типу long long без суфікса ll старші 32 біти ігноруються!',
                        invariant: 'Компілятор розгортає це в апаратні команди POPCNT / BSF / BSR / LZCNT.',
                        contest_trap: 'Виклик __builtin_clz(0) або __builtin_ctz(0) повертає Undefined Behavior!',
                        code_snippet: 'int bits = __builtin_popcountll(mask);\nint lowest_bit_idx = (mask > 0) ? __builtin_ctzll(mask) : -1;'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        macro_id: 'macro_tactics',
        macro_title: '7. Олімпіадна Тактика, Граблі та Стрес-Тестування',
        description: 'Бойові прийоми, налаштування компілятора, анти-баг чек-листи та пошук контрприкладів.',
        topics: [
          {
            topic_id: 'tactics_stress_testing',
            topic_title: 'Стрес-тестування (Fuzzing & Verification)',
            subtopics: [
              {
                subtopic_id: 'tactics_tree_generator',
                subtopic_title: 'Генерація випадкових дерев та зв\'язних графів',
                microtopics: [
                  {
                    micro_id: 'micro_random_tree_prufer',
                    micro_title: 'Генератор випадкових дерев різної топології (ланцюг, зірка, бамбук)',
                    nanotopics: [
                      {
                        nano_id: 'nano_bamboo_vs_star_trap',
                        nano_title: 'Спеціальні тести проти рекурсивного переповнення стеку (Stack Overflow)',
                        summary: 'Глибокий ланцюг довжиною 200,000 спричиняє переповнення стеку при рекурсивному DFS у C++ на Windows.',
                        invariant: 'Коректний розв\'язок повинен проходити і зірку (максимальний степінь O(N)), і бамбук (максимальна глибина O(N)).',
                        contest_trap: 'Випадкове дерево parent[i] = rand(1, i-1) має очікувану глибину лише O(log N) і не ловить stack overflow!',
                        code_snippet: '// Генерація бамбука:\nfor (int i = 2; i <= N; ++i) add_edge(i - 1, i);\n// Генерація зірки:\nfor (int i = 2; i <= N; ++i) add_edge(1, i);'
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            topic_id: 'tactics_submit_checklist',
            topic_title: 'Чек-лист перед здачею (Pre-Submit Checklist)',
            subtopics: [
              {
                subtopic_id: 'tactics_overflow_traps',
                subtopic_title: 'Анти-Overflow та Граничні випадки',
                microtopics: [
                  {
                    micro_id: 'micro_pre_submit_audit',
                    micro_title: 'Швидкий аудит коду перед кнопкою Submit',
                    nanotopics: [
                      {
                        nano_id: 'nano_1ll_shift_trap',
                        nano_title: 'Зсув 1LL << k замість 1 << k',
                        summary: 'У виразі 1 << 35 1 є 32-бітним int, що веде до невизначеної поведінки (UB).',
                        invariant: 'Будь-який бітовий зсув на k >= 31 зобов\'язаний оперувати 64-бітним типом 1ULL або 1LL.',
                        contest_trap: 'Помилка компілюється без попереджень, але повертає від\'ємні числа або 0 під час контесту.',
                        code_snippet: 'long long mask = (1LL << k);'
                      },
                      {
                        nano_id: 'nano_fast_io_sync',
                        nano_title: 'Розрив синхронізації ios_base::sync_with_stdio(0); cin.tie(0);',
                        summary: 'Прискорює роботу cin/cout у 5-10 разів, вирівнюючи швидкість із scanf/printf.',
                        invariant: 'Після виклику суворо заборонено змішувати cin з scanf/getchar.',
                        contest_trap: 'Використання std::endl замість \\n форсує очищення буфера (flush) і призводить до TLE.',
                        code_snippet: 'ios_base::sync_with_stdio(false);\ncin.tie(nullptr);\ncout.tie(nullptr);'
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ];

    // Classic Skill Tree Taxonomy (View 1)
    const SKILLS_DATA = [
      { id: 'prefix_sums', cat: 'basics', tier: 1, title: 'Префіксні суми та різницевий масив', desc: 'Швидкий підрахунок сум на відрізках за O(1) та масове додавання до підвідрізка за O(1).', practice: ['CSES: Subarray Sums II', 'LeetCode: 560. Subarray Sum Equals K', 'Codeforces: Kuriyama Mirai\'s Stones'] },
      { id: 'two_pointers', cat: 'basics', tier: 1, title: 'Два вказівники та Ковзне вікно', desc: 'Пошук підмасивів або пар із монотонною властивістю за лінійний час O(N).', practice: ['CSES: 2Sum & 3Sum', 'LeetCode: 3. Longest Substring Without Repeating Characters', 'Codeforces: 600B'] },
      { id: 'binary_search', cat: 'basics', tier: 1, title: 'Бінарний пошук по відповіді (Bisection)', desc: 'Пошук оптимального значення, коли функція перевірки check(mid) монотонна за O(log(MAX)).', practice: ['CSES: Factory Machines', 'LeetCode: 875. Koko Eating Bananas', 'Codeforces: Step 2 Edu BS'] },
      { id: 'greedy', cat: 'basics', tier: 2, title: 'Жадібні стратегії та Сортування', desc: 'Вибір локального оптимуму, доведення коректності обміном елементів (exchange argument).', practice: ['CSES: Movie Festival', 'LeetCode: 435. Non-overlapping Intervals', 'Codeforces: 1141D'] },

      { id: 'dp_1d2d', cat: 'dp', tier: 1, title: 'Базове 1D / 2D Динамічне Програмування', desc: 'Формування станів, базові переходи, відновлення відповіді, простір станів.', practice: ['CSES: Coin Combinations I & II', 'LeetCode: 198. House Robber', 'CSES: Grid Paths'] },
      { id: 'dp_knapsack', cat: 'dp', tier: 2, title: 'Задача про рюкзак (0/1 та Необмежений)', desc: 'Оптимізація пам\'яті до одновимірного масиву, зворотний обхід, відновлення набору предметів.', practice: ['CSES: Book Shop', 'LeetCode: 416. Partition Equal Subset Sum', 'AtCoder: Educational DP D & E'] },
      { id: 'dp_lis_lcs', cat: 'dp', tier: 2, title: 'LIS / LCS (Найдовша зростаюча підпослідовність)', desc: 'LIS за O(N log N) через двійковий пошук, LCS за O(N*M).', practice: ['CSES: Increasing Subsequence', 'LeetCode: 300. Longest Increasing Subsequence', 'CSES: Edit Distance'] },
      { id: 'dp_bitmask', cat: 'dp', tier: 3, title: 'ДП по бітових масках (Bitmask DP)', desc: 'Розв\'язання експоненційних задач (Комівояжер TSP, паросполучення) за O(2^N * N).', practice: ['CSES: Matching', 'AtCoder: DP O (Matching)', 'LeetCode: 847. Shortest Path Visiting All Nodes'] },
      { id: 'dp_tree', cat: 'dp', tier: 3, title: 'ДП на деревах (Tree DP)', desc: 'Обхід DFS знизу вгору, підрахунок діаметра, вибір максимальної незалежної множини.', practice: ['CSES: Tree Distances I & II', 'CSES: Subtree Queries', 'Codeforces: 161D'] },
      { id: 'dp_digit', cat: 'dp', tier: 3, title: 'Digit DP (ДП по цифрах числа)', desc: 'Підрахунок чисел у діапазоні [L, R] із певними властивостями цифр за O(D * S).', practice: ['CSES: Counting Numbers', 'LeetCode: 902. Numbers At Most N Given Digit Set', 'SPOJ: CPCRC1C'] },

      { id: 'graph_traversal', cat: 'graphs', tier: 1, title: 'BFS та DFS обходи графів', desc: 'Пошук компонент зв\'язності, перевірка на дводольність, 0-1 BFS.', practice: ['CSES: Counting Rooms', 'CSES: Message Route', 'CSES: Building Roads'] },
      { id: 'graph_dijkstra', cat: 'graphs', tier: 2, title: 'Алгоритм Дейкстри з priority_queue', desc: 'Найкоротші шляхи у графі з додатними вагами за O(M log N).', practice: ['CSES: Shortest Routes I', 'LeetCode: 743. Network Delay Time', 'Codeforces: 20C'] },
      { id: 'graph_floyd_bellman', cat: 'graphs', tier: 2, title: 'Флойд-Воршелл та Беллман-Форд', desc: 'Найкоротші шляхи між усіма парами вершин O(N^3) та від\'ємні цикли.', practice: ['CSES: Shortest Routes II', 'CSES: High Score', 'CSES: Cycle Finding'] },
      { id: 'graph_topo_dsu', cat: 'graphs', tier: 2, title: 'Топологічне сортування та DSU (Union-Find)', desc: 'DSU з евристикою рангу та стисненням шляху за майже O(1) (alpha(N)).', practice: ['CSES: Course Schedule', 'CSES: Road Reparation', 'LeetCode: 684. Redundant Connection'] },
      { id: 'graph_mst', cat: 'graphs', tier: 2, title: 'Мінімальний кістяк (Kruskal / Prim)', desc: 'Побудова мінімального кістякового дерева за O(M log M).', practice: ['CSES: Road Reparation', 'Codeforces: 1245D', 'LeetCode: 1584. Min Cost to Connect All Points'] },
      { id: 'graph_flow', cat: 'graphs', tier: 3, title: 'Максимальний потік (Dinic / Edmonds-Karp)', desc: 'Мережі, залишкова пропускна здатність, теорема про максимальний потік і мінімальний розріз.', practice: ['CSES: Download Speed', 'CSES: Police Chase', 'CSES: Distinct Routes'] },

      { id: 'ds_monostack', cat: 'ds', tier: 1, title: 'Монотонний стек та черга', desc: 'Next Greater Element за O(N), максимальний прямокутник у гістограмі.', practice: ['LeetCode: 739. Daily Temperatures', 'LeetCode: 84. Largest Rectangle in Histogram', 'CSES: Nearest Smaller Values'] },
      { id: 'ds_fenwick', cat: 'ds', tier: 2, title: 'Дерево Фенвіка (Binary Indexed Tree)', desc: 'Суми на префіксах і точкові оновлення за O(log N) у 10 рядків коду.', practice: ['CSES: Dynamic Range Sum Queries', 'Codeforces: 276C', 'CSES: Forest Queries II'] },
      { id: 'ds_segtree', cat: 'ds', tier: 2, title: 'Дерево відрізків (Segment Tree)', desc: 'Запити на відрізку (Min, Max, Sum, GCD) та модифікація в точці за O(log N).', practice: ['CSES: Dynamic Range Minimum Queries', 'Codeforces EDU: Segment Tree Part 1', 'CSES: Hotel Queries'] },
      { id: 'ds_lazy_segtree', cat: 'ds', tier: 3, title: 'Дерево відрізків з відкладеними операціями (Lazy)', desc: 'Масове оновлення на відрізку [L, R] та запити за O(log N).', practice: ['CSES: Range Update Queries', 'Codeforces EDU: Segment Tree Part 2', 'CSES: Polynomial Queries'] },
      { id: 'ds_trie', cat: 'ds', tier: 2, title: 'Бор (Trie) та XOR-Trie', desc: 'Пошук слів за префіксом та пошук пари з максимальним XOR за O(30 * N).', practice: ['CSES: Word Combinations', 'LeetCode: 421. Maximum XOR of Two Numbers', 'CSES: Bit Problem'] },

      { id: 'math_sieve', cat: 'math', tier: 1, title: 'Решето Ератосфена та факторизація', desc: 'Знаходження всіх простих до N за O(N log log N) або лінійне решето за O(N).', practice: ['CSES: Counting Divisors', 'CSES: Common Divisors', 'CSES: Prime Multiples'] },
      { id: 'math_modulo', cat: 'math', tier: 1, title: 'Модулярна арифметика та Швидке піднесення до степеня', desc: 'Обчислення (A^B) % MOD за O(log B), Мала теорема Ферма та модулярний обернений елемент.', practice: ['CSES: Exponentiation I & II', 'LeetCode: 50. Pow(x, n)', 'CSES: Creating Strings II'] },
      { id: 'math_combinatorics', cat: 'math', tier: 2, title: 'Комбінаторика: C(n, k) за O(1)', desc: 'Попередній розрахунок факторіалів та обернених факторіалів за модулем 10^9+7.', practice: ['CSES: Distributing Apples', 'CSES: Binomial Coefficients', 'CSES: Christmas Party'] },
      { id: 'math_matrix_expo', cat: 'math', tier: 3, title: 'Матричне швидке множення', desc: 'Обчислення N-го числа Фібоначчі або переходів лінійних рекурент за O(K^3 log N).', practice: ['CSES: Fibonacci Numbers', 'CSES: Graph Paths I & II', 'Codeforces: 185A'] },

      { id: 'str_hashing', cat: 'strings', tier: 1, title: 'Поліноміальне хешування рядків', desc: 'Порівняння підрядків за O(1) за модулями (подвійний хеш проти колізій).', practice: ['CSES: String Matching', 'CSES: Finding Borders', 'LeetCode: 214. Shortest Palindrome'] },
      { id: 'str_kmp_z', cat: 'strings', tier: 2, title: 'Префікс-функція (KMP) та Z-функція', desc: 'Пошук зразка у тексті за гарантований лінійний час O(N + M).', practice: ['CSES: String Matching', 'CSES: Minimal Rotation', 'Codeforces: 126B Password'] },
      { id: 'str_aho_corasick', cat: 'strings', tier: 3, title: 'Автомат Ахо-Корасік', desc: 'Одночасний пошук множини зразків у тексті за O(N + Sum |P_i|).', practice: ['CSES: Word Combinations', 'Codeforces: 1400F', 'SPOJ: SUBLEX'] },

      { id: 'tactics_stress_testing', cat: 'contest', tier: 1, title: 'Стрес-тестування та Fuzzing (scripts/stress_tester.py)', desc: 'Швидке написання тупого перебору O(N^2) та рандомайзера тестів для пошуку контрприкладів.', practice: ['Регулярна практика на контестах Codeforces Div.2/3'] },
      { id: 'tactics_edge_cases', cat: 'contest', tier: 1, title: 'Чек-лист граничних випадків (Edge Cases)', desc: 'Перевірка N=0,1, переповнення int32 -> int64, однакових елементів, від\'ємних чисел, порожніх графів.', practice: ['Submit Checklist перед кожною відправкою'] }
    ];

    const CATEGORIES = {
      basics: { name: 'Базові методи & Ad-Hoc', icon: 'zap', color: 'blue' },
      dp: { name: 'Динамічне Програмування (DP)', icon: 'layers', color: 'purple' },
      graphs: { name: 'Теорія Графів', icon: 'network', color: 'emerald' },
      ds: { name: 'Структури Даних', icon: 'box', color: 'amber' },
      math: { name: 'Математика & Комбінаторика', icon: 'hash', color: 'rose' },
      strings: { name: 'Алгоритми на Рядках', icon: 'type', color: 'cyan' },
      contest: { name: 'Контест-тактика & Тестування', icon: 'shield-check', color: 'indigo' }
    };

    const DEFAULT_TEAM = [
      {
        id: 'm1',
        name: 'Олександр (Капітан)',
        role: 'Графи & ДП',
        skills: {
          'prefix_sums': { status: 3, solved: 15, notes: 'Впевнено володіє 1D та 2D' },
          'two_pointers': { status: 3, solved: 12, notes: '' },
          'binary_search': { status: 3, solved: 20, notes: 'Часто вирішує задачі на монотонність' },
          'dp_1d2d': { status: 2, solved: 14, notes: '' },
          'dp_knapsack': { status: 2, solved: 8, notes: '' },
          'graph_traversal': { status: 3, solved: 18, notes: '' },
          'graph_dijkstra': { status: 2, solved: 10, notes: '' },
          'ds_segtree': { status: 1, solved: 4, notes: 'Потрібно попрактикувати масові оновлення' },
          'tactics_stress_testing': { status: 2, solved: 5, notes: '' }
        },
        nanos: {
          'nano_submask_idiom': true,
          'nano_dijkstra_stale_pair_check': true,
          'nano_dijkstra_long_long': true,
          'nano_bs_mid_overflow': true,
          'nano_1ll_shift_trap': true
        }
      },
      {
        id: 'm2',
        name: 'Марія',
        role: 'Математика & Рядки',
        skills: {
          'prefix_sums': { status: 2, solved: 10, notes: '' },
          'math_sieve': { status: 3, solved: 14, notes: 'Лінійне решето знає напам\'ять' },
          'math_modulo': { status: 3, solved: 12, notes: '' },
          'math_combinatorics': { status: 3, solved: 16, notes: '' },
          'math_matrix_expo': { status: 2, solved: 6, notes: '' },
          'str_hashing': { status: 2, solved: 8, notes: '' },
          'str_kmp_z': { status: 2, solved: 7, notes: '' },
          'binary_search': { status: 2, solved: 9, notes: '' }
        },
        nanos: {
          'nano_break_on_divisibility': true,
          'nano_inv_fact_stepback': true,
          'nano_random_base_chrono': true
        }
      },
      {
        id: 'm3',
        name: 'Дмитро',
        role: 'Структури Даних & Тестер',
        skills: {
          'prefix_sums': { status: 2, solved: 8, notes: '' },
          'two_pointers': { status: 2, solved: 10, notes: '' },
          'ds_monostack': { status: 3, solved: 12, notes: '' },
          'ds_fenwick': { status: 3, solved: 15, notes: '' },
          'ds_segtree': { status: 3, solved: 22, notes: 'Пише ДО за 3 хвилини' },
          'ds_lazy_segtree': { status: 2, solved: 9, notes: '' },
          'ds_trie': { status: 2, solved: 7, notes: '' },
          'tactics_stress_testing': { status: 3, solved: 20, notes: 'Майстер швидких генераторів' },
          'tactics_edge_cases': { status: 3, solved: 25, notes: '' }
        },
        nanos: {
          'nano_lazy_assignment_vs_addition': true,
          'nano_segtree_4n_bound': true,
          'nano_dsu_no_path_compression': true,
          'nano_bamboo_vs_star_trap': true,
          'nano_fast_io_sync': true
        }
      }
    ];

    let teamData = JSON.parse(localStorage.getItem('super_algo_team') || 'null') || DEFAULT_TEAM;
    let currentMemberId = teamData[0]?.id || 'm1';
    let currentCategoryFilter = 'all';
    let currentSearchQuery = '';
    let currentDecompSearch = '';
    let currentModalSkill = null;
    let radarChartInstance = null;

    function saveState() {
      localStorage.setItem('super_algo_team', JSON.stringify(teamData));
    }

    function getCurrentMember() {
      return teamData.find(m => m.id === currentMemberId) || teamData[0];
    }

    // View Switching
    const viewTabTree = document.getElementById('viewTabTree');
    const viewTabDecomp = document.getElementById('viewTabDecomp');
    const viewTabMindMap = document.getElementById('viewTabMindMap');
    const sectionTree = document.getElementById('sectionTree');
    const sectionDecomposition = document.getElementById('sectionDecomposition');
    const sectionMindMap = document.getElementById('sectionMindMap');

    function setActiveView(tabName) {
      // Reset classes
      viewTabTree.className = 'flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-gray-400 hover:text-white transition';
      viewTabDecomp.className = 'flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-gray-400 hover:text-white transition';
      viewTabMindMap.className = 'flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-gray-400 hover:text-white transition';

      sectionTree.classList.add('hidden');
      sectionDecomposition.classList.add('hidden');
      sectionMindMap.classList.add('hidden');

      if (tabName === 'tree') {
        viewTabTree.className = 'flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 text-white shadow-sm transition';
        sectionTree.classList.remove('hidden');
      } else if (tabName === 'decomp') {
        viewTabDecomp.className = 'flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-purple-600 text-white shadow-sm transition';
        sectionDecomposition.classList.remove('hidden');
        renderDecompositionTree();
      } else if (tabName === 'mindmap') {
        viewTabMindMap.className = 'flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-amber-600 text-white shadow-sm transition';
        sectionMindMap.classList.remove('hidden');
        if (window.mermaid) mermaid.run();
      }
      lucide.createIcons();
    }

    viewTabTree.onclick = () => setActiveView('tree');
    viewTabDecomp.onclick = () => setActiveView('decomp');
    viewTabMindMap.onclick = () => setActiveView('mindmap');

    // Mind Map Sub-tabs
    const mmBtnDecision = document.getElementById('mmBtnDecision');
    const mmBtnStage1 = document.getElementById('mmBtnStage1');
    const mmBtnPractice = document.getElementById('mmBtnPractice');
    const mmDiagDecision = document.getElementById('mmDiagramDecision');
    const mmDiagStage1 = document.getElementById('mmDiagramStage1');
    const mmDiagPractice = document.getElementById('mmDiagramPractice');

    function switchMindMap(mapType) {
      mmBtnDecision.className = 'px-3 py-1.5 rounded-lg font-bold text-gray-400 hover:text-white transition';
      mmBtnStage1.className = 'px-3 py-1.5 rounded-lg font-bold text-gray-400 hover:text-white transition';
      mmBtnPractice.className = 'px-3 py-1.5 rounded-lg font-bold text-gray-400 hover:text-white transition';

      mmDiagDecision.classList.add('hidden');
      mmDiagStage1.classList.add('hidden');
      mmDiagPractice.classList.add('hidden');

      if (mapType === 'decision') {
        mmBtnDecision.className = 'px-3 py-1.5 rounded-lg font-bold bg-amber-600 text-white transition';
        mmDiagDecision.classList.remove('hidden');
      } else if (mapType === 'stage1') {
        mmBtnStage1.className = 'px-3 py-1.5 rounded-lg font-bold bg-blue-600 text-white transition';
        mmDiagStage1.classList.remove('hidden');
      } else if (mapType === 'practice') {
        mmBtnPractice.className = 'px-3 py-1.5 rounded-lg font-bold bg-purple-600 text-white transition';
        mmDiagPractice.classList.remove('hidden');
      }
      if (window.mermaid) mermaid.run();
      lucide.createIcons();
    }

    mmBtnDecision.onclick = () => switchMindMap('decision');
    mmBtnStage1.onclick = () => switchMindMap('stage1');
    mmBtnPractice.onclick = () => switchMindMap('practice');

    // Render Members
    function renderMembers() {
      const list = document.getElementById('membersList');
      list.innerHTML = '';

      teamData.forEach(member => {
        const isActive = member.id === currentMemberId;
        const btn = document.createElement('button');
        btn.className = `w-full text-left p-2.5 rounded-xl border flex items-center justify-between transition ${
          isActive 
            ? 'bg-blue-600/15 border-blue-500/50 text-white glow-blue' 
            : 'bg-gray-800/40 border-gray-800 text-gray-300 hover:bg-gray-800/80 hover:border-gray-700'
        }`;
        btn.innerHTML = `
          <div class="flex items-center gap-2.5 truncate">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs ${
              isActive ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
            }">
              ${member.name.charAt(0)}
            </div>
            <div class="truncate">
              <div class="font-semibold text-xs truncate">${member.name}</div>
              <div class="text-[11px] text-gray-400 truncate">${member.role}</div>
            </div>
          </div>
          <i data-lucide="${isActive ? 'check-circle-2' : 'chevron-right'}" class="w-4 h-4 ${isActive ? 'text-blue-400' : 'text-gray-500'} shrink-0"></i>
        `;
        btn.onclick = () => {
          currentMemberId = member.id;
          renderMembers();
          renderStats();
          renderSkills();
          renderDecompositionTree();
        };
        list.appendChild(btn);
      });
      lucide.createIcons();
    }

    // Calculate Stats
    function renderStats() {
      const member = getCurrentMember();
      let masteredCount = 0;
      let totalSolved = 0;
      let scoreSum = 0;

      SKILLS_DATA.forEach(skill => {
        const state = member.skills?.[skill.id] || { status: 0, solved: 0 };
        if (state.status >= 2) masteredCount++;
        totalSolved += (state.solved || 0);
        scoreSum += (state.status || 0);
      });

      const nanosLearned = Object.keys(member.nanos || {}).filter(k => member.nanos[k]).length;
      document.getElementById('statNanoCount').textContent = nanosLearned;

      const maxScore = SKILLS_DATA.length * 2;
      const pct = Math.min(100, Math.round((scoreSum / maxScore) * 100));

      document.getElementById('memberProgressPct').textContent = `${pct}%`;
      document.getElementById('memberProgressBar').style.width = `${pct}%`;
      document.getElementById('statMasteredCount').textContent = masteredCount;

      const rankBadge = document.getElementById('memberRank');
      if (pct < 20) {
        rankBadge.textContent = 'Початківець';
        rankBadge.className = 'text-xs font-bold px-2 py-0.5 rounded bg-gray-700 text-gray-300 border border-gray-600';
      } else if (pct < 45) {
        rankBadge.textContent = 'Учень (Pupil)';
        rankBadge.className = 'text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
      } else if (pct < 70) {
        rankBadge.textContent = 'Спеціаліст (Specialist)';
        rankBadge.className = 'text-xs font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30';
      } else if (pct < 90) {
        rankBadge.textContent = 'Експерт (Expert)';
        rankBadge.className = 'text-xs font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30';
      } else {
        rankBadge.textContent = 'Кандидат у майстри';
        rankBadge.className = 'text-xs font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 glow-gold';
      }
    }

    // Render Classic Skills (View 1)
    function renderSkills() {
      const container = document.getElementById('skillsContainer');
      const member = getCurrentMember();
      container.innerHTML = '';
      const query = currentSearchQuery.toLowerCase().trim();

      Object.keys(CATEGORIES).forEach(catKey => {
        if (currentCategoryFilter !== 'all' && currentCategoryFilter !== catKey) return;
        const catMeta = CATEGORIES[catKey];
        const skillsInCat = SKILLS_DATA.filter(s => {
          if (s.cat !== catKey) return false;
          if (!query) return true;
          return s.title.toLowerCase().includes(query) || s.desc.toLowerCase().includes(query);
        });

        if (skillsInCat.length === 0) return;

        const section = document.createElement('div');
        section.className = 'flex flex-col gap-4';
        section.innerHTML = `
          <div class="flex items-center gap-2.5 pb-2 border-b border-algoBorder">
            <div class="p-1.5 rounded-lg bg-${catMeta.color}-500/20 text-${catMeta.color}-400">
              <i data-lucide="${catMeta.icon}" class="w-4 h-4"></i>
            </div>
            <h2 class="text-base font-bold text-white tracking-wide">${catMeta.name}</h2>
            <span class="text-xs text-gray-500 font-mono">(${skillsInCat.length})</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4" id="cat-grid-${catKey}"></div>
        `;

        container.appendChild(section);
        const grid = section.querySelector(`#cat-grid-${catKey}`);

        skillsInCat.forEach(skill => {
          const userState = member.skills?.[skill.id] || { status: 0, solved: 0, notes: '' };
          const card = document.createElement('div');

          let statusBorder = 'border-gray-800 bg-gray-900/60 hover:border-gray-700';
          let statusBadge = '<span class="text-[10px] px-2 py-0.5 rounded bg-gray-800 text-gray-400 border border-gray-700">Не вивчено</span>';
          let glowClass = '';

          if (userState.status === 1) {
            statusBorder = 'border-amber-500/40 bg-amber-950/10 hover:border-amber-500/60';
            statusBadge = '<span class="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">Теорія (50%)</span>';
          } else if (userState.status === 2) {
            statusBorder = 'border-emerald-500/40 bg-emerald-950/15 hover:border-emerald-500/60';
            statusBadge = '<span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Освоєно (100%)</span>';
            glowClass = 'glow-green';
          } else if (userState.status === 3) {
            statusBorder = 'border-purple-500/50 bg-purple-950/20 hover:border-purple-500/70';
            statusBadge = '<span class="text-[10px] px-2 py-0.5 rounded bg-purple-500/30 text-purple-200 border border-purple-500/40 font-semibold">Контест-майстер ⭐</span>';
            glowClass = 'glow-gold';
          }

          card.className = `border rounded-xl p-4 flex flex-col justify-between gap-3 cursor-pointer transition transform hover:-translate-y-0.5 ${statusBorder} ${glowClass}`;
          card.innerHTML = `
            <div class="flex flex-col gap-1.5">
              <div class="flex items-center justify-between gap-2">
                <span class="text-[11px] font-mono font-semibold text-gray-400">Tier ${skill.tier}</span>
                ${statusBadge}
              </div>
              <h3 class="text-sm font-bold text-white group-hover:text-blue-400 transition leading-snug">${skill.title}</h3>
              <p class="text-xs text-gray-400 line-clamp-2 leading-relaxed">${skill.desc}</p>
            </div>

            <div class="flex items-center justify-between pt-2 border-t border-gray-800/80 text-xs text-gray-400">
              <span class="flex items-center gap-1 font-mono text-[11px]">
                <i data-lucide="check-circle" class="w-3.5 h-3.5 text-amber-400"></i> ${userState.solved || 0} задач
              </span>
              <button class="cycle-status-btn text-xs text-blue-400 hover:text-blue-300 font-medium px-2 py-1 rounded bg-blue-500/10 border border-blue-500/20 transition">
                Змінити ↺
              </button>
            </div>
          `;

          card.onclick = (e) => {
            if (e.target.closest('.cycle-status-btn')) {
              userState.status = ((userState.status || 0) + 1) % 4;
              if (!member.skills) member.skills = {};
              member.skills[skill.id] = userState;
              saveState();
              renderStats();
              renderSkills();
              return;
            }
            openSkillModal(skill);
          };

          grid.appendChild(card);
        });
      });
      lucide.createIcons();
    }

    // Render 5-Level Ultra Decomposition (View 2)
    function renderDecompositionTree() {
      const container = document.getElementById('decompTreeContainer');
      container.innerHTML = '';
      const member = getCurrentMember();
      const q = currentDecompSearch.toLowerCase().trim();

      KNOWLEDGE_TREE.forEach(macro => {
        // Macro match check
        const macroCard = document.createElement('div');
        macroCard.className = 'border border-algoBorder bg-algoCard/70 rounded-2xl overflow-hidden shadow-lg';

        let totalMacroNanos = 0;
        let learnedMacroNanos = 0;

        // Traverse to count
        macro.topics.forEach(t => {
          t.subtopics.forEach(s => {
            s.microtopics.forEach(mi => {
              mi.nanotopics.forEach(na => {
                totalMacroNanos++;
                if (member.nanos?.[na.nano_id]) learnedMacroNanos++;
              });
            });
          });
        });

        const macroPct = totalMacroNanos > 0 ? Math.round((learnedMacroNanos / totalMacroNanos) * 100) : 0;

        macroCard.innerHTML = `
          <!-- Level 1: Macro Domain Header -->
          <div class="macro-header p-4.5 bg-gradient-to-r from-gray-900 to-gray-800/80 border-b border-algoBorder flex items-center justify-between cursor-pointer hover:bg-gray-800 transition">
            <div class="flex items-center gap-3">
              <span class="px-2 py-0.5 rounded-md bg-blue-600/30 text-blue-300 font-mono text-xs font-bold border border-blue-500/40">L1: МАКРО</span>
              <div>
                <h3 class="text-base font-bold text-white flex items-center gap-2">${macro.macro_title}</h3>
                <p class="text-xs text-gray-400 mt-0.5">${macro.description}</p>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-right">
                <div class="text-xs font-bold text-purple-400">${learnedMacroNanos} / ${totalMacroNanos} нано (${macroPct}%)</div>
                <div class="w-24 bg-gray-700 rounded-full h-1.5 mt-1 overflow-hidden">
                  <div class="bg-purple-500 h-1.5 rounded-full" style="width: ${macroPct}%"></div>
                </div>
              </div>
              <i data-lucide="chevron-down" class="w-5 h-5 text-gray-400 macro-arrow transition transform"></i>
            </div>
          </div>

          <!-- Topics Container -->
          <div class="macro-body p-4 flex flex-col gap-4">
            <!-- Topics rendered here -->
          </div>
        `;

        const macroBody = macroCard.querySelector('.macro-body');
        const macroHeader = macroCard.querySelector('.macro-header');
        const arrow = macroCard.querySelector('.macro-arrow');

        macroHeader.onclick = () => {
          macroBody.classList.toggle('hidden');
          arrow.classList.toggle('rotate-180');
        };

        // Render Level 2: Topics
        macro.topics.forEach(topic => {
          const topicCard = document.createElement('div');
          topicCard.className = 'border border-gray-800 bg-gray-900/50 rounded-xl p-4 flex flex-col gap-3.5';
          topicCard.innerHTML = `
            <div class="flex items-center gap-2 pb-2 border-b border-gray-800">
              <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-[11px] font-semibold border border-indigo-500/30">L2: ТЕМА</span>
              <h4 class="text-sm font-bold text-white">${topic.topic_title}</h4>
            </div>
            <div class="subtopics-container flex flex-col gap-4 pl-3 tree-line"></div>
          `;

          const subtopicsContainer = topicCard.querySelector('.subtopics-container');

          // Render Level 3: Subtopics
          topic.subtopics.forEach(subtopic => {
            const subtopicCard = document.createElement('div');
            subtopicCard.className = 'flex flex-col gap-3';
            subtopicCard.innerHTML = `
              <div class="flex items-center gap-2">
                <span class="px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 font-mono text-[10px] font-semibold border border-purple-500/30">L3: ПІДТЕМА</span>
                <h5 class="text-xs font-bold text-gray-200">${subtopic.subtopic_title}</h5>
              </div>
              <div class="microtopics-container flex flex-col gap-3 pl-3 tree-line"></div>
            `;

            const microContainer = subtopicCard.querySelector('.microtopics-container');

            // Render Level 4: Microtopics
            subtopic.microtopics.forEach(micro => {
              const microCard = document.createElement('div');
              microCard.className = 'flex flex-col gap-2.5';
              microCard.innerHTML = `
                <div class="flex items-center gap-2">
                  <span class="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[10px] font-semibold border border-emerald-500/30">L4: МІКРО</span>
                  <span class="text-xs font-semibold text-emerald-400">${micro.micro_title}</span>
                </div>
                <div class="nanotopics-grid grid grid-cols-1 md:grid-cols-2 gap-3 pl-3"></div>
              `;

              const nanoGrid = microCard.querySelector('.nanotopics-grid');

              // Render Level 5: Nanotopics
              micro.nanotopics.forEach(nano => {
                // Filter check
                if (q) {
                  const combinedText = `${macro.macro_title} ${topic.topic_title} ${subtopic.subtopic_title} ${micro.micro_title} ${nano.nano_title} ${nano.summary} ${nano.invariant} ${nano.contest_trap} ${nano.code_snippet}`.toLowerCase();
                  if (!combinedText.includes(q)) return;
                }

                const isLearned = member.nanos?.[nano.nano_id] || false;
                const nanoCard = document.createElement('div');
                nanoCard.className = `border rounded-xl p-3.5 flex flex-col justify-between gap-3 text-xs transition ${
                  isLearned 
                    ? 'border-emerald-500/50 bg-emerald-950/15 glow-green' 
                    : 'border-gray-800 bg-gray-950/60 hover:border-gray-700'
                }`;

                nanoCard.innerHTML = `
                  <div class="flex flex-col gap-2">
                    <div class="flex items-start justify-between gap-2">
                      <div class="flex items-center gap-1.5">
                        <span class="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-[10px] font-bold border border-amber-500/30">L5: НАНО</span>
                        <h6 class="font-bold text-white text-xs leading-snug">${nano.nano_title}</h6>
                      </div>
                      <button class="toggle-nano-btn shrink-0 px-2 py-0.5 rounded text-[10px] font-bold border transition ${
                        isLearned 
                          ? 'bg-emerald-500 text-white border-emerald-400' 
                          : 'bg-gray-800 text-gray-400 border-gray-700 hover:text-white'
                      }">
                        ${isLearned ? '✓ ЗАСВОЄНО' : '+ ВИВЧИТИ'}
                      </button>
                    </div>

                    <p class="text-gray-300 text-[11px] leading-relaxed">${nano.summary}</p>

                    <!-- Invariant Box -->
                    <div class="p-2 rounded-lg bg-blue-950/30 border border-blue-900/40 text-[11px]">
                      <span class="text-blue-300 font-bold block mb-0.5">💎 Інваріант:</span>
                      <span class="text-blue-200/80 font-mono text-[10px]">${nano.invariant}</span>
                    </div>

                    <!-- Contest Trap Box -->
                    <div class="p-2 rounded-lg bg-rose-950/30 border border-rose-900/40 text-[11px]">
                      <span class="text-rose-300 font-bold block mb-0.5">⚠️ Олімпіадні граблі (WA/TLE):</span>
                      <span class="text-rose-200/80 text-[10px]">${nano.contest_trap}</span>
                    </div>

                    <!-- Code Snippet -->
                    <div class="relative bg-black/60 rounded-lg p-2.5 font-mono text-[10px] text-emerald-300 border border-gray-800 overflow-x-auto custom-scroll">
                      <button class="copy-code-btn absolute right-2 top-2 p-1 rounded bg-gray-800 text-gray-400 hover:text-white transition" title="Копіювати">
                        <i data-lucide="copy" class="w-3 h-3"></i>
                      </button>
                      <pre><code>${nano.code_snippet}</code></pre>
                    </div>
                  </div>
                `;

                // Events
                const toggleBtn = nanoCard.querySelector('.toggle-nano-btn');
                toggleBtn.onclick = () => {
                  if (!member.nanos) member.nanos = {};
                  member.nanos[nano.nano_id] = !member.nanos[nano.nano_id];
                  saveState();
                  renderStats();
                  renderDecompositionTree();
                };

                const copyBtn = nanoCard.querySelector('.copy-code-btn');
                copyBtn.onclick = () => {
                  navigator.clipboard.writeText(nano.code_snippet);
                  copyBtn.innerHTML = '<span class="text-emerald-400 font-bold text-[9px]">OK!</span>';
                  setTimeout(() => {
                    copyBtn.innerHTML = '<i data-lucide="copy" class="w-3 h-3"></i>';
                    lucide.createIcons();
                  }, 1200);
                };

                nanoGrid.appendChild(nanoCard);
              });

              if (nanoGrid.children.length > 0) {
                microContainer.appendChild(microCard);
              }
            });

            if (microContainer.children.length > 0) {
              subtopicsContainer.appendChild(subtopicCard);
            }
          });

          if (subtopicsContainer.children.length > 0) {
            macroBody.appendChild(topicCard);
          }
        });

        if (macroBody.children.length > 0) {
          container.appendChild(macroCard);
        }
      });

      lucide.createIcons();
    }

    // Expand/Collapse All
    document.getElementById('expandAllDecompBtn').onclick = () => {
      document.querySelectorAll('.macro-body').forEach(b => b.classList.remove('hidden'));
      document.querySelectorAll('.macro-arrow').forEach(a => a.classList.add('rotate-180'));
    };
    document.getElementById('collapseAllDecompBtn').onclick = () => {
      document.querySelectorAll('.macro-body').forEach(b => b.classList.add('hidden'));
      document.querySelectorAll('.macro-arrow').forEach(a => a.classList.remove('rotate-180'));
    };

    // Live Decomp Search
    document.getElementById('decompSearchInput').oninput = (e) => {
      currentDecompSearch = e.target.value;
      renderDecompositionTree();
    };

    // Open Skill Modal
    function openSkillModal(skill) {
      currentModalSkill = skill;
      const member = getCurrentMember();
      const userState = member.skills?.[skill.id] || { status: 0, solved: 0, notes: '' };

      document.getElementById('modalTitle').textContent = skill.title;
      document.getElementById('modalDesc').textContent = skill.desc;
      document.getElementById('modalCategoryBadge').textContent = CATEGORIES[skill.cat].name;
      document.getElementById('modalTierBadge').textContent = `Tier ${skill.tier}`;

      const solved = userState.solved || 0;
      document.getElementById('modalSolvedCountDisplay').textContent = solved;
      document.getElementById('modalSolvedRange').value = solved;
      document.getElementById('modalNotes').value = userState.notes || '';
      updateModalStatusButtons(userState.status || 0);

      const pList = document.getElementById('modalPracticeList');
      pList.innerHTML = '';
      (skill.practice || []).forEach(p => {
        const item = document.createElement('div');
        item.className = 'p-2 bg-gray-800/60 rounded border border-gray-700/60 flex items-center justify-between text-gray-300';
        item.innerHTML = `<span>${p}</span><span class="text-[10px] text-blue-400 font-mono">Тренувати</span>`;
        pList.appendChild(item);
      });

      document.getElementById('skillModal').classList.remove('hidden');
    }

    let activeModalStatus = 0;
    function updateModalStatusButtons(status) {
      activeModalStatus = status;
      document.querySelectorAll('.status-select-btn').forEach(btn => {
        const s = parseInt(btn.dataset.status);
        if (s === status) {
          btn.classList.add('ring-2', 'ring-white', 'font-bold');
        } else {
          btn.classList.remove('ring-2', 'ring-white', 'font-bold');
        }
      });
    }

    document.querySelectorAll('.status-select-btn').forEach(btn => {
      btn.onclick = () => updateModalStatusButtons(parseInt(btn.dataset.status));
    });

    const solvedRange = document.getElementById('modalSolvedRange');
    const solvedDisplay = document.getElementById('modalSolvedCountDisplay');
    solvedRange.oninput = () => solvedDisplay.textContent = solvedRange.value;
    document.getElementById('incSolvedBtn').onclick = () => {
      solvedRange.value = Math.min(100, parseInt(solvedRange.value) + 1);
      solvedDisplay.textContent = solvedRange.value;
    };
    document.getElementById('decSolvedBtn').onclick = () => {
      solvedRange.value = Math.max(0, parseInt(solvedRange.value) - 1);
      solvedDisplay.textContent = solvedRange.value;
    };

    document.getElementById('saveModalBtn').onclick = () => {
      if (!currentModalSkill) return;
      const member = getCurrentMember();
      if (!member.skills) member.skills = {};
      member.skills[currentModalSkill.id] = {
        status: activeModalStatus,
        solved: parseInt(solvedRange.value),
        notes: document.getElementById('modalNotes').value.trim()
      };
      saveState();
      document.getElementById('skillModal').classList.add('hidden');
      renderStats();
      renderSkills();
    };

    document.getElementById('closeModalBtn').onclick = () => {
      document.getElementById('skillModal').classList.add('hidden');
    };

    // Category filter in View 1
    document.querySelectorAll('.cat-filter-btn').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.cat-filter-btn').forEach(b => {
          b.className = 'cat-filter-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition';
        });
        btn.className = 'cat-filter-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-blue-600 text-white transition';
        currentCategoryFilter = btn.dataset.cat;
        renderSkills();
      };
    });

    document.getElementById('searchInput').oninput = (e) => {
      currentSearchQuery = e.target.value;
      renderSkills();
    };

    // Add Member
    document.getElementById('addMemberBtn').onclick = () => {
      const name = prompt('Введіть ім\'я нового учасника команди:');
      if (!name) return;
      const role = prompt('Введіть спеціалізацію / роль (напр., ДП, Графи, Математика):') || 'Універсал';
      const newMember = {
        id: 'm_' + Date.now(),
        name: name.trim(),
        role: role.trim(),
        skills: {},
        nanos: {}
      };
      teamData.push(newMember);
      currentMemberId = newMember.id;
      saveState();
      renderMembers();
      renderStats();
      renderSkills();
      renderDecompositionTree();
    };

    // Team Radar Chart
    function renderRadarChart() {
      const ctx = document.getElementById('teamRadarCanvas').getContext('2d');
      const catKeys = Object.keys(CATEGORIES);
      const labels = catKeys.map(k => CATEGORIES[k].name);

      const colorPalettes = [
        { bg: 'rgba(59, 130, 246, 0.25)', border: '#3B82F6' },
        { bg: 'rgba(16, 185, 129, 0.25)', border: '#10B981' },
        { bg: 'rgba(245, 158, 11, 0.25)', border: '#F59E0B' },
        { bg: 'rgba(168, 85, 247, 0.25)', border: '#A855F7' }
      ];

      const datasets = teamData.map((member, idx) => {
        const palette = colorPalettes[idx % colorPalettes.length];
        const data = catKeys.map(catKey => {
          const skillsInCat = SKILLS_DATA.filter(s => s.cat === catKey);
          let sum = 0;
          skillsInCat.forEach(s => {
            sum += (member.skills?.[s.id]?.status || 0);
          });
          const max = skillsInCat.length * 3;
          return max > 0 ? Math.round((sum / max) * 100) : 0;
        });

        return {
          label: member.name,
          data: data,
          backgroundColor: palette.bg,
          borderColor: palette.border,
          borderWidth: 2,
          pointBackgroundColor: palette.border
        };
      });

      if (radarChartInstance) radarChartInstance.destroy();

      radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: { labels: labels, datasets: datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: { color: '#374151' },
              grid: { color: '#1F2937' },
              pointLabels: { color: '#9CA3AF', font: { size: 11, family: 'Plus Jakarta Sans' } },
              ticks: { backdropColor: 'transparent', color: '#6B7280', stepSize: 25, min: 0, max: 100 }
            }
          },
          plugins: {
            legend: { labels: { color: '#E2E8F0', font: { family: 'Plus Jakarta Sans' } } }
          }
        }
      });
    }

    document.getElementById('radarModalBtn').onclick = () => {
      document.getElementById('radarModal').classList.remove('hidden');
      renderRadarChart();
    };
    document.getElementById('closeRadarBtn').onclick = () => {
      document.getElementById('radarModal').classList.add('hidden');
    };

    // Export JSON
    document.getElementById('exportBtn').onclick = () => {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(teamData, null, 2));
      const a = document.createElement('a');
      a.setAttribute("href", dataStr);
      a.setAttribute("download", `super_algo_team_skills_${new Date().toISOString().slice(0,10)}.json`);
      document.body.appendChild(a);
      a.click();
      a.remove();
    };

    // Import JSON
    document.getElementById('importInput').onchange = (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const parsed = JSON.parse(event.target.result);
          if (Array.isArray(parsed)) {
            teamData = parsed;
            currentMemberId = teamData[0]?.id || 'm1';
            saveState();
            renderMembers();
            renderStats();
            renderSkills();
            renderDecompositionTree();
            alert('Дані команди успішно завантажено!');
          }
        } catch (err) {
          alert('Помилка читання JSON файлу!');
        }
      };
      reader.readAsText(file);
    };

    // Reset Data
    document.getElementById('resetBtn').onclick = () => {
      if (confirm('Скинути всі дані дерева до стандартних?')) {
        teamData = JSON.parse(JSON.stringify(DEFAULT_TEAM));
        currentMemberId = teamData[0].id;
        saveState();
        renderMembers();
        renderStats();
        renderSkills();
        renderDecompositionTree();
      }
    };

    // Init App
    renderMembers();
    renderStats();
    renderSkills();
  