#!/usr/bin/env python3
"""
Convertisseur XML WordPress vers Markdown avec interface graphique
Extrait les articles d'un export WordPress et les convertit en Markdown
"""

import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class HTMLToMarkdown(HTMLParser):
    """Convertit le HTML en Markdown"""
    
    def __init__(self):
        super().__init__()
        self.output = []
        self.current_tag = None
        self.link_url = None
        self.in_shortcode = False
        
    def handle_starttag(self, tag, attrs):
        """Gère les balises ouvrantes"""
        # Ignorer les shortcodes WordPress
        if tag.startswith('[') or self.in_shortcode:
            self.in_shortcode = True
            return
            
        # Ignorer les images
        if tag == 'img':
            return
            
        self.current_tag = tag
        
        # Gérer les liens
        if tag == 'a':
            for attr_name, attr_value in attrs:
                if attr_name == 'href':
                    self.link_url = attr_value
                    break
    
    def handle_endtag(self, tag):
        """Gère les balises fermantes"""
        # Fin d'un shortcode
        if tag.endswith(']'):
            self.in_shortcode = False
            return
            
        if tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.output.append('\n\n')
        elif tag == 'br':
            self.output.append('\n')
            
        if tag == 'a':
            self.link_url = None
            
        self.current_tag = None
    
    def handle_data(self, data):
        """Gère le contenu texte"""
        # Ignorer le contenu dans les shortcodes
        if self.in_shortcode:
            return
            
        # Ignorer le contenu vide
        data = data.strip()
        if not data:
            return
            
        # Appliquer le formatage selon la balise courante
        if self.current_tag == 'h1':
            self.output.append(f"# {data}")
        elif self.current_tag == 'h2':
            self.output.append(f"## {data}")
        elif self.current_tag == 'h3':
            self.output.append(f"### {data}")
        elif self.current_tag == 'h4':
            self.output.append(f"#### {data}")
        elif self.current_tag == 'h5':
            self.output.append(f"##### {data}")
        elif self.current_tag == 'h6':
            self.output.append(f"###### {data}")
        elif self.current_tag in ['strong', 'b']:
            self.output.append(f"**{data}**")
        elif self.current_tag in ['em', 'i']:
            self.output.append(f"*{data}*")
        elif self.current_tag == 'a' and self.link_url:
            self.output.append(f"[{data}]({self.link_url})")
        else:
            self.output.append(data)
    
    def get_markdown(self):
        """Retourne le markdown généré"""
        return ''.join(self.output)


def clean_shortcodes(content):
    """Supprime les shortcodes WordPress [et_pb_*] et similaires"""
    # Pattern pour les shortcodes avec attributs
    content = re.sub(r'\[et_pb_[^\]]*\]', '', content)
    # Pattern pour les shortcodes de fermeture
    content = re.sub(r'\[/et_pb_[^\]]*\]', '', content)
    # Pattern pour tous les autres shortcodes
    content = re.sub(r'\[[^\]]+\]', '', content)
    return content


def html_to_markdown(html_content):
    """Convertit le HTML en Markdown"""
    # Nettoyer les shortcodes WordPress
    html_content = clean_shortcodes(html_content)
    
    # Parser le HTML
    parser = HTMLToMarkdown()
    parser.feed(html_content)
    
    markdown = parser.get_markdown()
    
    # Nettoyer les espaces multiples et lignes vides excessives
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = re.sub(r' {2,}', ' ', markdown)
    
    return markdown.strip()


def extract_cdata(text):
    """Extrait le contenu d'une section CDATA"""
    if text and '<![CDATA[' in text:
        start = text.find('<![CDATA[') + 9
        end = text.rfind(']]>')
        if end > start:
            return text[start:end]
    return text


def parse_wordpress_xml(xml_file):
    """Parse le fichier XML WordPress et extrait les articles"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        raise Exception(f"Erreur lors du parsing XML : {e}")
    
    articles = []
    
    # Parcourir tous les items
    for item in root.findall('.//item'):
        article = {}
        
        # Extraire le titre
        title_elem = item.find('title')
        if title_elem is not None and title_elem.text:
            article['title'] = extract_cdata(title_elem.text)
        else:
            article['title'] = "Sans titre"
        
        # Extraire le lien
        link_elem = item.find('link')
        if link_elem is not None and link_elem.text:
            article['link'] = link_elem.text.strip()
        else:
            article['link'] = ""
        
        # Extraire le contenu
        # Chercher dans différents namespaces possibles
        content = None
        for content_tag in ['{http://purl.org/rss/1.0/modules/content/}encoded', 
                           'content:encoded', 
                           'encoded']:
            content_elem = item.find(content_tag)
            if content_elem is not None and content_elem.text:
                content = extract_cdata(content_elem.text)
                break
        
        if not content:
            # Essayer une recherche plus générale
            for elem in item:
                if 'encoded' in elem.tag.lower():
                    content = extract_cdata(elem.text) if elem.text else ""
                    break
        
        article['content'] = content if content else ""
        
        # Ajouter l'article si il a du contenu
        if article['title'] or article['content']:
            articles.append(article)
    
    return articles


def convert_to_markdown(articles):
    """Convertit tous les articles en un document Markdown"""
    markdown_parts = []
    
    for i, article in enumerate(articles):
        # Ajouter la ligne de séparation (sauf pour le premier article)
        if i > 0:
            markdown_parts.append("...\n")
        
        # Ajouter le titre
        markdown_parts.append(f"# {article['title']}\n")
        
        # Ajouter le lien
        if article['link']:
            markdown_parts.append(f"{article['link']}\n")
        
        # Convertir et ajouter le contenu
        if article['content']:
            markdown_content = html_to_markdown(article['content'])
            if markdown_content:
                markdown_parts.append(f"\n{markdown_content}")
        
        # Ajouter un saut de ligne entre les articles
        markdown_parts.append("\n")
    
    return '\n'.join(markdown_parts)


class WordPressConverter:
    """Interface graphique pour le convertisseur WordPress"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur XML WordPress vers Markdown")
        self.root.geometry("600x400")
        
        # Variables
        self.xml_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Convertisseur XML WordPress vers Markdown", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sélection du fichier XML d'entrée
        ttk.Label(main_frame, text="Fichier XML d'entrée:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.xml_file, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Parcourir...", command=self.select_xml_file).grid(row=1, column=2, padx=5)
        
        # Sélection du fichier Markdown de sortie
        ttk.Label(main_frame, text="Fichier Markdown de sortie:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Parcourir...", command=self.select_output_file).grid(row=2, column=2, padx=5)
        
        # Bouton de conversion
        self.convert_button = ttk.Button(main_frame, text="Convertir", command=self.start_conversion)
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Zone de texte pour les logs
        log_frame = ttk.LabelFrame(main_frame, text="Journal des opérations", padding="5")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def select_xml_file(self):
        """Sélectionne le fichier XML d'entrée"""
        filename = filedialog.askopenfilename(
            title="Sélectionner le fichier XML WordPress",
            filetypes=[("Fichiers XML", "*.xml"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.xml_file.set(filename)
            # Proposer automatiquement un nom de fichier de sortie
            if not self.output_file.get():
                output_name = filename.rsplit('.', 1)[0] + '.md'
                self.output_file.set(output_name)
    
    def select_output_file(self):
        """Sélectionne le fichier Markdown de sortie"""
        filename = filedialog.asksaveasfilename(
            title="Enregistrer le fichier Markdown",
            defaultextension=".md",
            filetypes=[("Fichiers Markdown", "*.md"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def log(self, message):
        """Ajoute un message au journal"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_conversion(self):
        """Démarre la conversion dans un thread séparé"""
        if not self.xml_file.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier XML d'entrée")
            return
        
        if not self.output_file.get():
            messagebox.showerror("Erreur", "Veuillez spécifier un fichier de sortie")
            return
        
        # Désactiver le bouton et démarrer la barre de progression
        self.convert_button.config(state='disabled')
        self.progress.start()
        self.log_text.delete(1.0, tk.END)
        
        # Lancer la conversion dans un thread séparé
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
    
    def convert_files(self):
        """Effectue la conversion"""
        try:
            self.log(f"Lecture du fichier XML : {self.xml_file.get()}")
            articles = parse_wordpress_xml(self.xml_file.get())
            self.log(f"Nombre d'articles trouvés : {len(articles)}")
            
            if not articles:
                self.log("Aucun article trouvé dans le fichier XML")
                messagebox.showwarning("Attention", "Aucun article trouvé dans le fichier XML")
                return
            
            self.log("Conversion en Markdown...")
            markdown_content = convert_to_markdown(articles)
            
            self.log(f"Écriture du fichier Markdown : {self.output_file.get()}")
            with open(self.output_file.get(), 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.log("Conversion terminée avec succès !")
            messagebox.showinfo("Succès", "La conversion s'est terminée avec succès !")
            
        except Exception as e:
            error_msg = f"Erreur lors de la conversion : {str(e)}"
            self.log(error_msg)
            messagebox.showerror("Erreur", error_msg)
        
        finally:
            # Réactiver le bouton et arrêter la barre de progression
            self.root.after(0, self.finish_conversion)
    
    def finish_conversion(self):
        """Termine la conversion (appelé dans le thread principal)"""
        self.progress.stop()
        self.convert_button.config(state='normal')


def main():
    """Fonction principale"""
    # Vérifier si on utilise la ligne de commande ou l'interface graphique
    if len(sys.argv) == 3:
        # Mode ligne de commande (comportement original)
        xml_file = sys.argv[1]
        output_file = sys.argv[2]
        
        print(f"Lecture du fichier XML : {xml_file}")
        articles = parse_wordpress_xml(xml_file)
        print(f"Nombre d'articles trouvés : {len(articles)}")
        
        if not articles:
            print("Aucun article trouvé dans le fichier XML")
            sys.exit(1)
        
        print("Conversion en Markdown...")
        markdown_content = convert_to_markdown(articles)
        
        print(f"Écriture du fichier Markdown : {output_file}")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Conversion terminée avec succès !")
        except IOError as e:
            print(f"Erreur lors de l'écriture du fichier : {e}")
            sys.exit(1)
    
    else:
        # Mode interface graphique
        root = tk.Tk()
        app = WordPressConverter(root)
        root.mainloop()


if __name__ == "__main__":
    main()
