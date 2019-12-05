(ns style.core
  (:require
   [reagent.core :as r]
   ))

(.log js/console "[init] style.core")


(defn stay-on-hash!
  "hacky way to prevent page from moving on toggle"
  []
  (def loc (.-hash (.-location js/window)))
  (.log js/console (.-hash js/location))
  (set! (.-hash js/location) loc))

(def menu-state (r/atom false))
(defn menu-toggle [state]
  (defonce toc (.getElementById js/document "table-of-contents"))
  (defonce pa (.getElementById js/document "postamble"))
  (defonce content (.getElementById js/document "content"))

  (defn unshow []
    (.add (.-classList toc) "unshow")
    (.add (.-classList pa) "unshow")
    (.add (.-classList content) "unshow"))
  (defn show []
    (.remove (.-classList toc) "unshow")
    (.remove (.-classList pa) "unshow")
    (.remove (.-classList content) "unshow"))
  (if state (show) (unshow))
  (if state false true))


(def home "https://simonwoodburyforget.github.io/mindustry-modding/")
(defn go-home []
  (set! (.-location js/window) home))

(defn button-component []
  [:div#toggle {:class (if @menu-state "unshow" "show")}
   [:button {:on-click #(swap! menu-state menu-toggle)} "☰"]
   ;; [:button {:on-click go-home } "⌂"]
   ])

(defn ^export run []
  (defonce app (.appendChild (.-body js/document)
                             (.createElement js/document "APP")))
  (r/render [button-component] app))

(set! (.-onload js/window) run)
