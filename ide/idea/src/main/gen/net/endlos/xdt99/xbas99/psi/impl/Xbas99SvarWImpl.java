// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99.psi.Xbas99Types.*;
import net.endlos.xdt99.xbas99.psi.*;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public class Xbas99SvarWImpl extends Xbas99NamedElementImpl implements Xbas99SvarW {

  public Xbas99SvarWImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99Visitor visitor) {
    visitor.visitSvarW(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99Visitor) accept((Xbas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xbas99FStr> getFStrList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99FStr.class);
  }

  @Override
  @NotNull
  public List<Xbas99Nexprn> getNexprnList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99Nexprn.class);
  }

  @Override
  @NotNull
  public List<Xbas99Sexpr> getSexprList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99Sexpr.class);
  }

  @Override
  @NotNull
  public List<Xbas99SvarR> getSvarRList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99SvarR.class);
  }

  @Override
  public @NotNull String getName() {
    return Xbas99PsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xbas99PsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xbas99PsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return Xbas99PsiImplUtil.getPresentation(this);
  }

  @Override
  public PsiReference getReference() {
    return Xbas99PsiImplUtil.getReference(this);
  }

}
