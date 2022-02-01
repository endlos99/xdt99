// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99l.psi.Xbas99LTypes.*;
import net.endlos.xdt99.xbas99l.psi.*;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public class Xbas99LNvarFImpl extends Xbas99LNamedElementImpl implements Xbas99LNvarF {

  public Xbas99LNvarFImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitNvarF(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99LVisitor) accept((Xbas99LVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xbas99LNvarW> getNvarWList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LNvarW.class);
  }

  @Override
  @NotNull
  public List<Xbas99LSvarW> getSvarWList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LSvarW.class);
  }

  @Override
  public @NotNull String getName() {
    return Xbas99LPsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xbas99LPsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xbas99LPsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return Xbas99LPsiImplUtil.getPresentation(this);
  }

  @Override
  public PsiReference getReference() {
    return Xbas99LPsiImplUtil.getReference(this);
  }

}
