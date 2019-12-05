(ns style.core
  (:require
   [reagent.core :as r]
   ))

(.log js/console "[init] style.core")

(defonce toc (.getElementById js/document "table-of-contents"))
(defonce pa (.getElementById js/document "postamble"))
(defonce content (.getElementById js/document "content"))
(defonce body (.getElementById js/document "content"))

(defonce app (.appendChild (.-body js/document)
                            (.createElement js/document "APP")))

(defn stay-on-hash!
  "hacky way to prevent page from moving on toggle"
  []
  (def loc (.-hash (.-location js/window)))
  (.log js/console (.-hash js/location))
  (set! (.-hash js/location) loc))

(def menu-state (r/atom false))
(defn menu-toggle [state]
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

(defn button-component []
  [:button#toggle {:class (if @menu-state "unshow" "show")
                   :on-click #(swap! menu-state menu-toggle)} "☰"])

(defn ^:export run []
  (r/render [button-component] app))

(run)
