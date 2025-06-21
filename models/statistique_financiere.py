import csv
from io import StringIO
from flask import Response
from flask_login import current_user
from flask import render_template, make_response
from xhtml2pdf import pisa
from io import BytesIO

try:
    from .depense import Depense
    from .revenu import Revenu
    from .categorie_depense import CategorieDepense
except ImportError:
    from depense import Depense
    from revenu import Revenu
    from categorie_depense import CategorieDepense

class StatistiqueFinanciere:
    def __init__(self, mois, annee):
        self.utilisateur_id = current_user.id_utilisateur
        self.mois = mois
        self.annee = annee
        self.revenus = Revenu.revenus_par_utilisateur_et_mois(self.utilisateur_id, mois, annee)
        self.depenses = Depense.depenses_par_utilisateur_et_mois(self.utilisateur_id, mois, annee)
        self.categories_depenses = CategorieDepense.lister_categorie_par_personne(self.utilisateur_id)

    def solde(self):
        return sum(r.montant for r in self.revenus) - sum(d.montant for d in self.depenses)

    def solde_par_categorie(self):
        resultats = {}
        for categorie in self.categories_depenses:
            montant_total = sum(
                d.montant for d in self.depenses if d.categorie == categorie.id_categorie
            )
            resultats[categorie.description] = {
                'id_categorie': categorie.id_categorie,
                'description': categorie.description,
                'total': montant_total,
                'limite': categorie.limite,
                'solde': round(categorie.limite - montant_total, 2)
            }
        return resultats


    
    def moyenne_depenses(self):
        if not self.depenses:
            return 0
        return round(sum(d.montant for d in self.depenses) / len(self.depenses), 2)

    def moyenne_revenus(self):
        if not self.revenus:
            return 0
        return round(sum(r.montant for r in self.revenus) / len(self.revenus), 2)
    
    def total_revenus(self):
        return sum(r.montant for r in self.revenus)

    def total_depenses(self):
        return sum(d.montant for d in self.depenses)
    
    
    def generer_csv(self):
        output = StringIO()
        writer = csv.writer(output)


        writer.writerow(["Statistiques financières"])
        writer.writerow(["Mois", self.mois])
        writer.writerow(["Année", self.annee])
        writer.writerow([])


        writer.writerow(["Totaux"])
        writer.writerow(["Total revenus (€)", self.total_revenus()])
        writer.writerow(["Total dépenses (€)", self.total_depenses()])
        writer.writerow(["Solde (€)", self.solde()])
        writer.writerow(["Moyenne revenus (€)", self.moyenne_revenus()])
        writer.writerow(["Moyenne dépenses (€)", self.moyenne_depenses()])
        writer.writerow([])


        writer.writerow(["Catégorie", "Total Dépensé (€)", "Limite (€)", "Solde (€)"])
        for categorie, data in self.solde_par_categorie().items():
            writer.writerow([
                categorie,
                data['total'],
                data['limite'],
                data['solde']
            ])


        output.seek(0)
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename=statistiques_{self.mois}_{self.annee}.csv"}
        )
    


    def generer_csv(self):
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["Statistiques financières"])
        writer.writerow(["Mois", self.mois])
        writer.writerow(["Année", self.annee])
        writer.writerow([])

        writer.writerow(["Totaux"])
        writer.writerow(["Total revenus (€)", self.total_revenus()])
        writer.writerow(["Total dépenses (€)", self.total_depenses()])
        writer.writerow(["Solde (€)", self.solde()])
        writer.writerow(["Moyenne revenus (€)", self.moyenne_revenus()])
        writer.writerow(["Moyenne dépenses (€)", self.moyenne_depenses()])
        writer.writerow([])

       
        writer.writerow(["Liste des revenus"])
        writer.writerow(["Date", "Description", "Montant (€)", "Catégorie"])
        for revenu in self.revenus:

            writer.writerow([
                getattr(revenu, "date", ""),
                getattr(revenu, "description", ""),
                getattr(revenu, "montant", ""),
                categorie
            ])
        writer.writerow([])

        # Liste des dépenses
        writer.writerow(["Liste des dépenses"])
        writer.writerow(["Date", "Description", "Montant (€)", "Catégorie"])
        for depense in self.depenses:
            try:
                categorie = depense.categorie.description if hasattr(depense, "categorie") else ""
            except:
                categorie = ""
            writer.writerow([
                getattr(depense, "date", ""),
                getattr(depense, "description", ""),
                getattr(depense, "montant", ""),
                categorie
            ])
        writer.writerow([])

        # Statistiques par catégorie
        writer.writerow(["Catégorie", "Total Dépensé (€)", "Limite (€)", "Solde (€)"])
        for categorie, data in self.solde_par_categorie().items():
            writer.writerow([
                categorie,
                data['total'],
                data['limite'],
                data['solde']
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename=statistiques_{self.mois}_{self.annee}.csv"}
        )


    def generer_pdf(self):
        html = render_template(
            "statistiques_pdf.html",
            mois=self.mois,
            annee=self.annee,
            solde=self.solde(),
            total_revenus=self.total_revenus(),
            total_depenses=self.total_depenses(),
            moyenne_revenus=self.moyenne_revenus(),
            moyenne_depenses=self.moyenne_depenses(),
            stats_categorie=self.solde_par_categorie()
        )

        result = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=result)

        if pisa_status.err:
            return f"Erreur PDF : {pisa_status.err}"

        response = make_response(result.getvalue())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"attachment; filename=statistiques_{self.mois}_{self.annee}.pdf"
        return response
