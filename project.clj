(defproject mindustry-mods "0.1.0-SNAPSHOT"
  :description "Mindustry-Mods listing html generation."
  :url "https://github.com/SimonWoodburyForget/mindustry-mods"
  :license {:name "GNU General Public License v3.0"}
  
  :dependencies [[org.clojure/clojure "1.10.1"]
                 [org.clojure/clojurescript "1.10.597"]
                 [reagent "0.9.0-rc3"]
                 ;; [cljs-ajax "0.8.0"]
                 ;; [hickory "0.7.1"]
                 [garden "1.3.9"]
                 ]

  :plugins [[lein-cljsbuild "1.1.7"]
            ;; [lein-figwheel "0.5.19"]
            ]

  ;; :clean-targets ^{:protect false}
  
  :source-paths ["helper"]
  :resource-paths ["."]
  ;; :figwheel {:http-server-root "."
  ;;            :css-dirs ["styles/main/css"]}

  :cljsbuild {:builds
              {:app {:source-paths ["helper"]
                     :compiler
                     {:main "style.core"
                      :output-to "styles/main/js/main.js"
                      :output-dir "styles/main/js/out"
                      ;; :asset-path "js/out"
                      :source-map true
                      :optimizations :none}
                     ;; :figwheel
                     ;; {;; :on-jsload "style.core/run"
                     ;;  :open-urls ["http://localhost:3449/index.html"]}
                     }

               :release {:source-paths ["helper"]
                         :compiler
                         {:output-to "styles/main/js/main.js"
                          :optimizations :advanced}}}})
